#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py loaddata core/fixtures/initial_team.json || true
python manage.py loaddata badges/fixtures/initial_badges.json || true
python manage.py collectstatic --noinput

