# Domain Club

A Django-powered Mathematics Club site with public content, student accounts, weekly 24-hour numerical puzzles, scores, streaks, badges, and leaderboards.

## Local setup

1. Create and activate a Python 3.10+ virtual environment.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set environment variables (or use development defaults).
4. `python manage.py migrate`
5. `python manage.py createsuperuser`
6. `python manage.py runserver`

Use `/admin/` to create staff-managed content, badges, and puzzles. A puzzle's end time is always computed as its start time plus 24 hours. Run `python manage.py process_puzzles` from a scheduled job after puzzles expire; it awards scores once, updates streaks/badges/monthly scores, and recalculates ranks.

## Production

Use PostgreSQL through `DATABASE_URL`, Gunicorn, `collectstatic`, secure environment variables, HTTPS, persistent media/object storage, and a scheduler that executes `process_puzzles` at least hourly. Never use Django's development server in production.
"# Domain-club" 
