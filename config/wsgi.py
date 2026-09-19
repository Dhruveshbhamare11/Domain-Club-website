import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
app = application

# Automatic startup database table initialization & static files collection
try:
    from django.core.management import call_command
    call_command("migrate", interactive=False)
except Exception as e:
    print(f"[WSGI Init] Migration notice: {e}")

try:
    from django.core.management import call_command
    call_command("collectstatic", interactive=False, clear=False)
except Exception as e:
    print(f"[WSGI Init] collectstatic notice: {e}")


