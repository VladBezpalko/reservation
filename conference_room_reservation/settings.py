import os
import sys
from datetime import time, timedelta

from getenv import env
from dj_database_url import parse as parse_db_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't6h#k9m_nt2_!=-g7&b!(z$zsqfcl!pjjlcf55q_^fd++!fyqv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',

    'reservation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conference_room_reservation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conference_room_reservation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASE_URL = env(
    'DATABASE_URL',
    default='postgres://admin:admin@localhost:5432/reservation',
)

DATABASES = {
    'default': parse_db_url(DATABASE_URL, conn_max_age=600),
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(levelname)s %(name)s %(asctime)s]: %(message)s'
        },
        'plain': {
            'format': '%(message)s'
        },
        'celery_task': {
            '()': 'celery.app.log.TaskFormatter',
            'fmt': '[%(levelname)s %(task_name)s %(asctime)s]: %(message)s',
            'use_color': False,
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': sys.stdout,
        },
        'print': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'plain',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
        },
        'django_extensions.management.commands.runserver_plus': {
            'propagate': False,
        },
        'django.security': {
            'handlers': ['null'],
            'propagate': False,
        },
        'celery.redirected': {
            'handlers': ['print'],
            'propagate': False,
        },
        'celery.task': {
            'handlers': ['console'],
            'propagate': False,
        },
        'werkzeug': {
            'propagate': False,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

REDIS_HOST = env('DEFAULT_REDIS_HOST', default='localhost')
REDIS_PORT = env('DEFAULT_REDIS_PORT', default=6379)
CELERY_REDIS_URL = 'redis://%s:%d/' % (REDIS_HOST, REDIS_PORT)

BROKER_URL = env('BROKER_URL', default=CELERY_REDIS_URL)
CELERY_RESULT_BACKEND = env(
    'CELERY_RESULT_BACKEND',
    default=CELERY_REDIS_URL,
)

CELERYBEAT_SCHEDULE = {
    'delete-old-records': {
        'task': 'reservation.tasks.delete_old_records',
        'schedule': timedelta(days=30),
    },
}

# Reservation settings
WORK_HOURS = (time(8, 30), time(17, 30))
MIN_TIME_BEFORE_RESERVATION = timedelta(minutes=30)
MINIMUM_MEETING_DURATION = timedelta(minutes=20)
MAXIMUM_MEETING_DURATION = timedelta(hours=3)
