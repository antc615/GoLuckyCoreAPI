"""
Django settings for GoLuckyCoreAPI project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""


from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'users.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ze3&!-xe^-!254#i3p6g8jz9yc11w^g+t-0qgsnp*qkzqy6fsc"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'channels',
    'apps.users',
    'apps.matches',
    'apps.chat',
    'apps.notifications',
    'apps.interactions'
]

ASGI_APPLICATION = 'GoLuckyCoreAPI.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Default host and port for Redis
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "GoLuckyCoreAPI.urls"

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

WSGI_APPLICATION = "GoLuckyCoreAPI.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'golucky',
        'USER': 'dev',
        'PASSWORD': 'dev123',
        'HOST': 'localhost',  # Set to empty string for localhost
        'PORT': '',           # Set to empty string for default
    },
    # 'cassandra': {
    #     'ENGINE': 'django_cassandra_engine',
    #     'NAME': 'golucky',
    #     'TEST_NAME': 'test_golucky',
    #     'HOST': '127.0.0.1',  # Or your Cassandra cluster address
    #     'OPTIONS': {
    #         'replication': {
    #             'strategy_class': 'SimpleStrategy',
    #             'replication_factor': 1
    #         }
    #     }
    # }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Access token valid for 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=24),  # Example: Refresh token valid for 1 hours
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'antc615@gmail.com'
EMAIL_HOST_PASSWORD = 'jdsj kzml zczm edww'

AUTHENTICATION_BACKENDS = [
    'apps.users.authentication.AllowInactiveUserModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Celery Configuration Options
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'

#CASSANDRA VARS
CASSANDRA_CLUSTER_NODES = ['127.0.0.1']  # list of IPs
CASSANDRA_KEYSPACE = 'golucky'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Maximum size, in bytes, of a request before it will be streamed to the file system instead of into memory.
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # Example: 2.5 MB

# Maximum size in bytes that a request's body may be before a SuspiciousOperation (RequestDataTooBig) is raised.
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # Example: 5 MB