#!/bin/bash
# Stop at the first failing step so a broken build never goes live.
set -e

# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

# Migrations are committed in the repo; the build only applies them.
echo "Apply migrations..."
python3.9 manage.py migrate --noinput

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear
