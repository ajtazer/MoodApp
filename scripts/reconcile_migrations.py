"""Record social.0010/0011 as applied when their tables already exist.

An old Vercel build generated its own (never committed) migration that created
social_post, social_post_liked_by and social_comment, so the committed 0010 and
0011 were never recorded and `migrate` fails with "relation already exists".

This only fakes them when every table and column they create is present; if
anything is missing it exits non-zero and the build stops. Data is untouched.
Run with: python manage.py shell < scripts/reconcile_migrations.py
"""
import sys

from django.core.management import call_command
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

EXPECTED = {
    'social_post': {'id', 'user', 'image', 'caption', 'created', 'likes'},
    'social_post_liked_by': {'id', 'post_id', 'user_id'},
    'social_comment': {'id', 'text', 'created', 'post_id', 'user_id'},
}

applied = {name for app, name in MigrationRecorder(connection).applied_migrations() if app == 'social'}
pending = [m for m in ('0010_auto_20250407_1507', '0011_auto_20250407_1521') if m not in applied]

with connection.cursor() as cursor:
    tables = set(connection.introspection.table_names(cursor))
    if not pending or 'social_post' not in tables:
        print('reconcile: nothing to do')
        sys.exit(0)
    for table, columns in EXPECTED.items():
        if table not in tables:
            print(f'reconcile: {table} is missing, not faking anything')
            sys.exit(1)
        have = {c.name for c in connection.introspection.get_table_description(cursor, table)}
        if not columns <= have:
            print(f'reconcile: {table} lacks {sorted(columns - have)}, not faking anything')
            sys.exit(1)

for name in pending:
    print(f'reconcile: tables already exist, recording social.{name} as applied')
    call_command('migrate', 'social', name, fake=True, verbosity=1)
