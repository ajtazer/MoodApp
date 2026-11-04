#!/bin/bash
# Vercel build step: install Python dependencies, apply migrations, collect static files.
# Each step exits with its own code, so a failed deploy says which step broke:
#   11 no Python found, 12 could not set up pip, 13 pip install, 14 migrate, 15 collectstatic,
#   16 secret key missing, 17 database unreachable, 18 schema mismatch, 19 legacy post import

PY=$(command -v python3.9 || command -v python3 || true)
[ -n "$PY" ] || { echo "No Python interpreter found"; exit 11; }
echo "Using $PY ($("$PY" --version 2>&1))"

# Work in a virtualenv; the build image may ship Python without pip.
VENV=/tmp/moodapp-build-venv
"$PY" -m venv "$VENV" >/dev/null 2>&1 || "$PY" -m venv --without-pip "$VENV" || exit 12
VPY="$VENV/bin/python"
if ! "$VPY" -m pip --version >/dev/null 2>&1; then
  echo "pip missing, bootstrapping it"
  curl -fsSL https://bootstrap.pypa.io/pip/3.9/get-pip.py -o /tmp/get-pip.py || exit 12
  "$VPY" /tmp/get-pip.py --quiet || exit 12
fi

echo "Installing dependencies..."
"$VPY" -m pip install --quiet -r requirements.txt || exit 13

#   16 DJANGO_SECRET_KEY missing at build time, 17 cannot connect to the database
[ -n "$DJANGO_SECRET_KEY" ] || { echo "DJANGO_SECRET_KEY is not set for this environment"; exit 16; }
"$VPY" manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('database reachable:', connection.vendor)" || exit 17

# One-off repair for the live database (see scripts/reconcile_migrations.py).  18 = schema mismatch
"$VPY" manage.py shell < scripts/reconcile_migrations.py > /tmp/step.log 2>&1 || { cat /tmp/step.log; exit 18; }
cat /tmp/step.log

# Migrations are committed in the repo; the build only applies them.
echo "Applying migrations..."
"$VPY" manage.py migrate --noinput > /tmp/step.log 2>&1 || { cat /tmp/step.log; exit 14; }
cat /tmp/step.log

# Bring the two old local posts into the live feed (skips them once imported).  19 = import failed
"$VPY" manage.py shell < scripts/import_legacy_posts.py || exit 19

echo "Collecting static files..."
"$VPY" manage.py collectstatic --noinput --clear || exit 15
