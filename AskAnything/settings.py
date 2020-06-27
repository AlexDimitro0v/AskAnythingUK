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
import django_heroku
import json
# Load the file that contains the sensitive information
# with open('config.json') as config_file:
#     config = json.load(config_file)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


LOGIN_REDIRECT_URL = 'home-page'  # By default when logged in Django looks for a route in accounts/profile
LOGIN_URL = 'login-page'          # Useful when login_required decorator is used; by default Django looks for a route in accounts/login
LOGOUT_REDIRECT_URL = 'landing-page'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['ask-anything-uk.herokuapp.com', 'http://www.realaskanything.com/', 'localhost', '127.0.0.1']


# Application definition
# By default Django looks for a template subdir in each of our installed aps !!!
# That's why anytime we create a new app we should add it to the list, so that Django can correctly search for templates
# and modules (which deal with the databases)
INSTALLED_APPS = [
    'crispy_forms',              # used to make forms more beautiful
    'phonenumber_field',         # used to ensure real numbers are provided
    'sweetify',                  # used for the alerts
    'django_cleanup',            # to auto-delete old media files (like old profile images)
    'users.apps.UsersConfig',
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mailer',                    # used for the sending of emails
    'multiforloop',              # allows having nested loops
    'django_elasticsearch_dsl',  # wrapper used for searching
    'django_user_agents',        # used for fraud prevention
    'coverage',                  # used for testing
    'django_nose',               # allows to run a specific test
    'storages',                  # allows us to store static files (files and images) on AWS
    'sendgrid'
]


ES_URL = os.environ.get('BONSAI_URL')

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': ES_URL
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
                'main.context_processors.notifications_processor',
                'main.context_processors.logged_in_universal_processor'
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
        'NAME': 'AskAnything',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD'),    # Note that you should use the password you set for your DB !!!!!!!
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


# Increases security
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'


# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# In order to website can find the media when we try to view them from within the browser, adjust:
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    # where Django will store uploaded files (in the base dir -> media dir)
MEDIA_URL = '/media/'                           # how we will access our media through the browser


CRISPY_TEMPLATE_PACK = 'bootstrap4'     # Crispy Forms will be using Bootstrap for styling
SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'


# Email Server (Using SendGrid SMTP)
# EMAIL_BACKEND = "mailer.backend.DbBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

# Email Server (Using SendGrid)
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = os.environ.get("SENDGRID_USERNAME")
# EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD")
EMAIL_FROM = "teamalpha050@gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Braintree Payment Gateway Keys
BRAINTREE_PUBLIC_KEY = os.environ.get('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = os.environ.get('BRAINTREE_PRIVATE_KEY')
BRAINTREE_MERCHANT_KEY = os.environ.get('BRAINTREE_MERCHANT_KEY')


# AWS Keys
# Used to store all of the media files (profile images and files) on AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
AWS_S3_FILE_OVERWRITE = False                                       # DO NOT OVERWRITE FILES WITH THE SAME NAMES
AWS_DEFAULT_ACL = None


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'   # To upload the media files to S3 directly
django_heroku.settings(locals())
