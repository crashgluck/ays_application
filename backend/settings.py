import os
from pathlib import Path

try:
    import pymysql
except ImportError:
    pymysql = None
else:
    pymysql.install_as_MySQLdb()


BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


IS_WINDOWS = os.name == "nt"
IS_PRODUCTION = env_bool("DJANGO_PRODUCTION", default=not IS_WINDOWS)
DEBUG = env_bool("DJANGO_DEBUG", default=not IS_PRODUCTION)

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-ck_i6!m75=zvry&&^g^ly8blop&czioberm&74@8-_)2t+nns&",
)

default_hosts = "aguasyservicioslaz.cl,www.aguasyservicioslaz.cl,s480.v2nets.com,localhost,127.0.0.1"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", default_hosts).split(",")
    if host.strip()
]

csrf_origins = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").strip()
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins.split(",") if origin.strip()]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "landing_page",
    "reportes",
    "noticias",
    "accounts",
    "tarifas_condiciones",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "backend.middleware.StaticCacheControlMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.user_access_flags",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"


USE_REMOTE_DB = env_bool("USE_REMOTE_DB", default=IS_PRODUCTION)

if IS_WINDOWS and not USE_REMOTE_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "aguasyse_ays_database"),
            "USER": os.getenv("DB_USER", "aguasyse_admin"),
            "PASSWORD": os.getenv("DB_PASSWORD", "xd21proclus"),
            "HOST": os.getenv("DB_HOST", "s480.v2nets.com"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "es"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = Path(
    os.getenv(
        "DJANGO_STATIC_ROOT",
        str(BASE_DIR / "staticfiles") if IS_WINDOWS else "/home/aguasyse/public_html/static/",
    )
)

if IS_PRODUCTION:
    USE_MANIFEST_STATIC = env_bool("DJANGO_USE_MANIFEST_STATIC", False)
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": (
                "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
                if USE_MANIFEST_STATIC
                else "django.contrib.staticfiles.storage.StaticFilesStorage"
            )
        },
    }

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(
    os.getenv(
        "DJANGO_MEDIA_ROOT",
        str(BASE_DIR / "media") if IS_WINDOWS else "/home/aguasyse/public_html/media/",
    )
)


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/report-views/"
LOGOUT_REDIRECT_URL = "/"


# In local development we default to console backend to avoid SMTP failures.
# In production we keep SMTP as default.
EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
    if IS_PRODUCTION
    else "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "25"))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", False)
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "lecturas@aguasyservicioslaz.cl")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "lecturas2024")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
SERVER_EMAIL = os.getenv("SERVER_EMAIL", EMAIL_HOST_USER)
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "30"))


LOG_FILE_PATH = Path(
    os.getenv(
        "DJANGO_LOG_FILE",
        str(BASE_DIR / "django_errors.log") if IS_WINDOWS else "/home/aguasyse/django_errors.log",
    )
)
try:
    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
except OSError:
    LOG_FILE_PATH = BASE_DIR / "django_errors.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE_PATH),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        }
    },
}

if DEBUG:
    LOGGING["handlers"]["console"] = {
        "level": "INFO",
        "class": "logging.StreamHandler",
    }
    LOGGING["loggers"]["django"]["handlers"].append("console")

if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
    SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
    SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
