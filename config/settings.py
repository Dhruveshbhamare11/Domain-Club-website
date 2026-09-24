import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env variables if file exists
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip()
                if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                    v = v[1:-1]
                if k not in os.environ or not os.environ[k]:
                    os.environ[k] = v

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-development-key-change-me")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS_RAW = os.getenv("ALLOWED_HOSTS", "")
if ALLOWED_HOSTS_RAW:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_RAW.split(",") if host.strip()]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com", ".vercel.app", "*"]

for host in [".vercel.app", "localhost", "127.0.0.1"]:
    if host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

CSRF_TRUSTED_ORIGINS_RAW = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if CSRF_TRUSTED_ORIGINS_RAW:
    CSRF_TRUSTED_ORIGINS = [url.strip() for url in CSRF_TRUSTED_ORIGINS_RAW.split(",") if url.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        "https://*.onrender.com",
        "https://*.vercel.app",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

if "https://*.vercel.app" not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append("https://*.vercel.app")

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "django.contrib.sites", "django.contrib.sitemaps",
    "core", "accounts", "puzzles", "leaderboard", "badges", "events", "blog",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True, "OPTIONS": {"context_processors": [
        "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database Configuration (Supabase PostgreSQL / Cloud DB / SQLite fallback)
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if DATABASE_URL:
    is_transaction_pooler = ":6543" in DATABASE_URL
    # Session mode (port 5432) or standard connection supports persistent conn_max_age (300s).
    # This avoids full SSL/TLS handshakes on every web request, drastically speeding up response times.
    conn_max_age_default = 0 if is_transaction_pooler else 300
    conn_max_age = int(os.getenv("DB_CONN_MAX_AGE", str(conn_max_age_default)))
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=conn_max_age,
            conn_health_checks=True,
            disable_server_side_cursors=is_transaction_pooler,
            ssl_require=True if ("supabase" in DATABASE_URL or "postgres" in DATABASE_URL) else False,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 6}},
]
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us").strip() or "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata").strip() or "Asia/Kolkata"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles_build" / "static"
try:
    os.makedirs(STATIC_ROOT, exist_ok=True)
except OSError:
    pass

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
WHITENOISE_USE_FINDERS = False
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0

# High-Performance In-Memory Cache (Eliminates repeated DB hits across page navigations)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "domain-club-fast-cache",
        "TIMEOUT": 60,
    }
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "accounts:login"
AUTHENTICATION_BACKENDS = ["accounts.backends.EmailOrUsernameBackend"]
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"
SITE_ID = 1

# Production Reverse Proxy & SSL Configuration (Render / Railway / Heroku / Vercel)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG and not os.getenv("DISABLE_SSL_REDIRECT", "")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

