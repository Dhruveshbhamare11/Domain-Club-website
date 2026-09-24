#!/usr/bin/env bash
set -e

echo "--> [Vercel Build] Determining python binary..."
if command -v python3.11 &> /dev/null; then
    PYTHON=python3.11
elif command -v python3 &> /dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

echo "--> [Vercel Build] Using $PYTHON"
$PYTHON -m pip install --upgrade pip || true
$PYTHON -m pip install -r requirements.txt

echo "--> [Vercel Build] Collecting static files..."
$PYTHON manage.py collectstatic --noinput --clear

echo "--> [Vercel Build] Finished successfully!"

