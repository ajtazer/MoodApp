"""Record social migrations as applied when their tables already exist.

An old Vercel build generated its own (never committed) migration that created
social_post, so the committed 0010 was never recorded and `migrate` fails with
'relation "social_post" already exists'. 0011 (likes + comments) never ran.

Each migration is faked only when every table and column it creates is present;
a migration whose tables are partly present stops the build. Migrations whose
tables are absent are left for `migrate` to apply normally. Data is untouched.
Run with: python manage.py shell < scripts/reconcile_migrations.py
"""
import sys

from django.core.management import call_command
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

CREATES = {
    '0010_auto_20250407_1507': {
        'social_post': {'id', 'user', 'image', 'caption', 'created', 'likes'},
    },
    '0011_auto_20250407_1521': {
        'social_post_liked_by': {'id', 'post_id', 'user_id'},
        'social_comment': {'id', 'text', 'created', 'post_id', 'user_id'},
    },
}

applied = {name for app, name in MigrationRecorder(connection).applied_migrations() if app == 'social'}

with connection.cursor() as cursor:
    tables = set(connection.introspection.table_names(cursor))
    to_fake = []
    for name, creates in CREATES.items():
        if name in applied:
            continue
        present = [t for t in creates if t in tables]
        if not present:
            break  # this and later migrations run normally
        if len(present) != len(creates):
            print(f'reconcile: {name} is half-applied ({present}), not faking anything')
            sys.exit(1)
        for table, columns in creates.items():
            have = {c.name for c in connection.introspection.get_table_description(cursor, table)}
            if not columns <= have:
                print(f'reconcile: {table} lacks {sorted(columns - have)}, not faking anything')
                sys.exit(1)
        to_fake.append(name)

if not to_fake:
    print('reconcile: nothing to do')
for name in to_fake:
    print(f'reconcile: tables for social.{name} already exist, recording it as applied')
    call_command('migrate', 'social', name, fake=True, verbosity=1)
