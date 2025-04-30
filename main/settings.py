from pathlib import Path
import os
import json

from celery.schedules import crontab
from dotenv import load_dotenv
from os.path import join, dirname
from datetime import timedelta

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

BASE_DIR = Path(__file__).resolve().parent.parent

HOST_IP = os.environ.get("HOST_IP", "localhost")
HOST_NAME = os.environ.get("HOST_NAME", "schedula.catholic-u.ai")
DB_HOST = os.environ.get("DB_HOST", "localhost")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "superman")


REDIS_USERNAME = "guest"
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB_CELERY = 1
REDIS_DB_RESULT = 1
REDIS_DB_CACHE = 3


# Maximum size (in bytes) that a request can be before raising a SuspiciousOperation (413) error.
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB

# Maximum size (in bytes) that a file can be before it gets streamed to the file system.
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_files"),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CORS_ORIGIN_WHITELIST = [
    "127.0.0.1:8080",
    "http://localhost:8080",
    "https://localhost:8080",
    f"http://{HOST_IP}:8080",
    f"https://{HOST_IP}:8080",
    f"http://{HOST_NAME}",
    f"https://{HOST_NAME}",
]

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    HOST_IP,
    HOST_NAME,
]


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080",
    "https://127.0.0.1:8080",
    "http://localhost:8080",
    "https://localhost:8080",
    f"http://{HOST_IP}:8080",
    f"https://{HOST_IP}:8080",
    f"http://{HOST_NAME}",
    f"https://{HOST_NAME}",
]


CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8080",
    "https://127.0.0.1:8080",
    f"http://{HOST_IP}:8080",
    f"https://{HOST_IP}:8080",
    "http://localhost:8080",
    "https://localhost:8080",
    f"http://{HOST_NAME}",
    f"https://{HOST_NAME}",
]


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1
SECURE_SSL_REDIRECT = "True"
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_COOKIE_SECURE = True


customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "template_partials",
    "crispy_forms",
    "crispy_bootstrap5",
    "crispy_tailwind",
    "widget_tweaks",
    "django_tables2",
    "django_filters",
    "django_extensions",
    "tailwind",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.apple",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
    "django_celery_beat",
    "django_celery_results",
    "corsheaders",
    "channels",
    "core",
    "polls",
]
# ASGI_APPLICATION = 'main.routing.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

TAILWIND_APP_NAME = "theme"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",  # HTMX Middleware
    "allauth.account.middleware.AccountMiddleware",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                # ... any other loaders ...
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "main.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "vul_schedula",
        "USER": "postgres",
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": "postgres",
        "PORT": 5432,
    }
}


AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_TZ = True
USE_I18N = True
CELERY_TIMEZONE = "America/New_York"
CELERY_ENABLE_UTC = False


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = True
EMAIL_PORT = 465
AUTH_USER_MODEL = "core.User"

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_CELERY}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_RESULT}"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/{}".format(REDIS_HOST, REDIS_PORT, REDIS_DB_CACHE),
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/{}".format(REDIS_HOST, REDIS_PORT, REDIS_DB_CACHE),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

CELERY_BEAT_SCHEDULE = {}


SECRET_KEY = "django-secure-hs6j037urx7iav+7#10%-vu4l4f5@@-1_zo)oft3g8$vf2$jmp"
DJANGO_DEBUG = "true"
SELECT2_CACHE_BACKEND = "select2"
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
