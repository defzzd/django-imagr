"""
Django settings for imagr_site project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import credentials
credentials.set_credentials()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8#o%qk@i&hk=3u3xs)sn_7_!tr5b+f_heai1875_9qk5$2r!ti'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

#LOGIN_URL = '/'
#LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = 'imagr_app:front_page'

MEDIA_ROOT = 'imagr_app/static'

#MEDIA_URL = 'imagr_app/static/'

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_HOST = 'smtp.mailgun.org'

EMAIL_HOST_USER = 'postmaster@sandboxc05c58d13d3143b5a761460872fadcbc.mailgun.org'

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagr_app',
    'registration'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'imagr_site.urls'

WSGI_APPLICATION = 'imagr_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'imagr',
        'USER': 'imagr',
        'PASSWORD': 'imagr',
        'HOST': 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'imagr_app.ImagrUser'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
