#!/usr/bin/env bash
set -e

export PIP_BREAK_SYSTEM_PACKAGES=1

echo "--> [Vercel Build] Determining python binary..."
if command -v python3.11 &> /dev/null; then
    PYTHON=python3.11
elif command -v python3 &> /dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

echo "--> [Vercel Build] Using $PYTHON"

if command -v uv &> /dev/null; then
    echo "--> [Vercel Build] Installing dependencies using uv..."
    uv pip install -r requirements.txt --system || uv pip install -r requirements.txt --break-system-packages
else
    echo "--> [Vercel Build] Installing dependencies using pip..."
    $PYTHON -m pip install -r requirements.txt --break-system-packages
fi

echo "--> [Vercel Build] Collecting static files..."
$PYTHON manage.py collectstatic --noinput --clear

echo "--> [Vercel Build] Finished successfully!"


