"""
Django settings for AskAnything project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/

# Quick-start development settings - unsuitable for production see:
# https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
"""

import os
import json
# Load the file that contains the sensitive information
#with open('config.json') as config_file:
#    config = json.load(config_file)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


LOGIN_REDIRECT_URL = 'home-page'  # By default when logged in Django looks for a route in accounts/profile
LOGIN_URL = 'login-page'          # Useful when login_required decorator is used; by default Django looks for a route in accounts/login
# LOGOUT_REDIRECT_URL = 'logout-page'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "^m5ounntw1@bdo&07@o85^ia68iqod++@=hah95#ypaljj8w&0"
# SECRET_KEY = config['DJANGO_SECRET_KEY']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
# By default Django looks for a template subdir in each of our installed aps !!!
# That's why anytime we create a new app we should add it to the list, so that Django can correctly search for templates
# and modules (which deal with the databases)
INSTALLED_APPS = [
    'crispy_forms',
    'django_cleanup',           # to auto-delete old media files (like old profile images)
    'users.apps.UsersConfig',
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'multiforloop'
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

ROOT_URLCONF = 'AskAnything.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'main.templatetags'
        ],
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

WSGI_APPLICATION = 'AskAnything.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ask_anything',
        'USER': 'postgres',
        'PASSWORD': 1234,                           # Note that you should use the password you set for your DB !!!!!!!
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'


# In order to website can find the media when we try to view them from within the browser, adjust:
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    # where Django will store uploaded files (in the base dir -> media dir)
MEDIA_URL = '/media/'                           # how we will access our media through the browser


CRISPY_TEMPLATE_PACK = 'bootstrap4'     # Crispy Forms will be using Bootstrap for styling


# Email Server (Using Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "teamalpha050@gmail.com"
EMAIL_HOST_PASSWORD = "AlphaTeam123"
