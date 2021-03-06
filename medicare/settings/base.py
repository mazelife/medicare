import os


"""
Django settings common to all instances of the project.

For more information on this file, see
https://docs.djangoproject.com/en//topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en//ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# The project directory -- two directories up from this file.
PROJECT_DIR = os.path.normpath(os.path.join(BASE_DIR, os.pardir))


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        from django.core.exceptions import ImproperlyConfigured
        error_msg = "The {0} environment variable is not set".format(var_name)
        raise ImproperlyConfigured(error_msg)


# Load dotCloud env file variables.
#import json
#
#def get_env_variable(var_name):
#    """ Get the environment variable from the dotCloud env. """
#    with open('/home/dotcloud/environment.json') as f:
#        env = json.load(f)
#        try:
#            return env[var_name]
#        except KeyError:
#            from django.core.exceptions import ImproperlyConfigured
#            error_msg = "The {0} environment variable is not set".format(var_name)
#            raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en//howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'medicare.hospitals',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'medicare.urls'

WSGI_APPLICATION = 'medicare.wsgi.application'


# Database
# https://docs.djangoproject.com/en//ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "medicare.db"
    }
}

# Internationalization
# https://docs.djangoproject.com/en//topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en//howto/static-files/

STATIC_URL = '/static/'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

# Template files.
# https://docs.djangoproject.com/en//#the-template-layer

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

# The Bing maps API key used for geocoding.
BING_GEOCODE_API_KEY = get_env_variable("BING_GEOCODE_API_KEY")

# If using less, sass or coffeescript...
#COMPRESS_PRECOMPILERS = (
#    ('text/coffeescript', 'coffee --compile --stdio'),
#    ('text/less', 'lessc {infile} {outfile}'),
#    ('text/x-sass', 'sass {infile} {outfile}'),
#    ('text/x-scss', 'sass --scss {infile} {outfile}'),
#)
