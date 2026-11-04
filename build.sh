#!/bin/bash
# Vercel build step: install Python dependencies, apply migrations, collect static files.
# Each step exits with its own code, so a failed deploy says which step broke:
#   11 no Python found, 12 could not set up pip, 13 pip install, 14 migrate, 15 collectstatic

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

# Migrations are committed in the repo; the build only applies them.
echo "Applying migrations..."
"$VPY" manage.py migrate --noinput || exit 14

echo "Collecting static files..."
"$VPY" manage.py collectstatic --noinput --clear || exit 15
