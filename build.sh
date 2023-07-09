#!/bin/bash

# Build the project
echo "Building the project..."
python3 -m pip install -r requirements.txt

echo "Collect Static..."
python3 manage.py collectstatic --noinput --clear

echo "Make Migration..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
