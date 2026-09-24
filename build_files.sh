#!/usr/bin/env bash
set -e

export PIP_BREAK_SYSTEM_PACKAGES=1

echo "--> [Vercel Build] Python version:"
python3 --version

echo "--> [Vercel Build] Installing dependencies from requirements.txt..."
python3 -m pip install -r requirements.txt --break-system-packages

echo "--> [Vercel Build] Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "--> [Vercel Build] Build finished successfully!"


