web: python manage.py migrate --noinput && python manage.py loaddata core/fixtures/initial_team.json && python manage.py loaddata badges/fixtures/initial_badges.json && python manage.py collectstatic --noinput && gunicorn config.wsgi:application


