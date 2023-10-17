"""
Django settings for Ecolog_django project.
Generated by 'django-admin startproject' using Django 4.1.2.
For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from os import getenv
from dotenv import load_dotenv

# from secrets import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
load_dotenv(BASE_DIR / 'config//django_settings//.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if getenv("DEBUG").lower() in ('true', '1') else False

ALLOWED_HOSTS = [getenv("MAIN_HOST")]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "eco.apps.EcoConfig",
    "rest_framework",
    "review.apps.ReviewConfig",
    "users.apps.UsersConfig",
    "report.apps.ReportConfig",
    "activities.apps.ActivitiesConfig",
    "base.apps.BaseConfig",
    "user_profiles.apps.UserProfilesConfig",
    "favorites.apps.FavoritesConfig",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "smart_selects",
    "debug_toolbar",
]

#Убрал csrf-токен, при необходимости вернуть!
#'django.middleware.csrf.CsrfViewMiddleware'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'Ecolog_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Ecolog_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        "NAME": getenv("NAME_DB"),
        "USER": getenv("USERNAME_DB"),
        "PASSWORD": getenv("PASSWORD_DB"),
        "HOST": getenv("HOST_DB"),
        "PORT": getenv("PORT_DB"),
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / 'ecolog',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static_django/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_django')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'eco.CustomUser'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,

    "TOKEN_REFRESH_SERIALIZER":'users.serializers.CustomTokenRefreshSerializer',
}

SECURE_COOKIE = getenv('SECURE_COOKIE')

#Небезопасно убрать!
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = (
    #Убрать(надо разделить тестовый и прод сервера)
    'http://localhost:8080',
    'http://81.163.30.36',
    'http://aurasolution.ru',
    'https://localhost:8080',
)

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

INTERNAL_IPS = [
    # ...
    getenv("MAIN_HOST"),
    # ...
]


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'base.pagination.DefaultProjectPagination',
}