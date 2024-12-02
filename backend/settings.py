from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-&&_@zzj-w3je738%&(r&3b6_&%3g@_dzwl0r-_^@fji+fi$*)q"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "users",
    "corsheaders",
    "rest_framework_simplejwt",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware", 
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


CORS_ALLOW_ALL_ORIGINS = True  
CORS_ALLOW_CREDENTIALS = True  
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000", 
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# JWT Authentication settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication", 
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated", 
    ),
}

# SimpleJWT settings for token expiration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1), 
    "ROTATE_REFRESH_TOKENS": True,  
    "BLACKLIST_AFTER_ROTATION": True, 
    "AUTH_HEADER_TYPES": ("Bearer",), 
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

STRIPE_SECRET_KEY = "sk_test_51OdzTIFpiA74WvTWt0Iz15c8lw5FGx1H0LKT8HW9J6e2EYzd7NizPKlQD6UI0QozMpwgJFeNLYNgs1G3dA8S7NMd00zN8JP5Um"
STRIPE_PUBLISHABLE_KEY = "pk_test_51OdzTIFpiA74WvTWxmL6JVHTYuvqp95ur8Zz4J0Hw28gGP4Md7S3J0EhvnjLoECfrSBSjaG6z532sEL1Y7nF3qiY00YyPq9654"
STRIPE_WEBHOOK_SECRET = "your_webhook_secret_here"  # Optional, for webhooks
