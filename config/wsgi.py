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

# Automatic data seeding if Team is empty
try:
    from core.models import TeamMember
    if TeamMember.objects.count() == 0:
        from django.core.management import call_command
        call_command("loaddata", "core/fixtures/initial_team.json")
        print("[WSGI Init] Loaded 16 team members successfully!")
except Exception as e:
    print(f"[WSGI Init] TeamMember load notice: {e}")

# Automatic data seeding if Badges are empty
try:
    from badges.models import Badge
    if Badge.objects.count() == 0:
        from django.core.management import call_command
        call_command("loaddata", "badges/fixtures/initial_badges.json")
        print("[WSGI Init] Loaded badges successfully!")
except Exception as e:
    print(f"[WSGI Init] Badge load notice: {e}")

try:
    from django.core.management import call_command
    call_command("collectstatic", interactive=False, clear=False)
except Exception as e:
    print(f"[WSGI Init] collectstatic notice: {e}")

# Automatic superuser creation if none exists
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        admin_user = os.getenv("DJANGO_SUPERUSER_USERNAME", "dhruvesh")
        admin_email = os.getenv("DJANGO_SUPERUSER_EMAIL", "nanapatil3636@gmail.com")
        admin_pass = os.getenv("DJANGO_SUPERUSER_PASSWORD", "DomainClub@2026!")
        User.objects.create_superuser(username=admin_user, email=admin_email, password=admin_pass)
        print(f"[WSGI Init] Superuser '{admin_user}' initialized successfully!")
except Exception as e:
    print(f"[WSGI Init] Superuser create notice: {e}")




