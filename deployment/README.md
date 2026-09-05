# Deployment

Set `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS`. Run `deployment/build.sh`, serve `config.wsgi` through Gunicorn, and schedule `python manage.py process_puzzles` at least hourly. Persist `MEDIA_ROOT` or use object storage in production.
