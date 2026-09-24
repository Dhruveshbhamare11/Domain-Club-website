#!/usr/bin/env bash
# Vercel Build Script for Django
set -e

echo "--> [Vercel Build] Installing python dependencies..."
python3 -m pip install -r requirements.txt

echo "--> [Vercel Build] Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "--> [Vercel Build] Applying database migrations..."
python3 manage.py migrate --noinput || true

echo "--> [Vercel Build] Completed successfully!"
