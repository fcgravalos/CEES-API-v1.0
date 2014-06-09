"""
Django settings for cees project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9q5@ow5%%2_oy5235-%n-#+xot!iy@@9#kapc8jhccqs+p1#6!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'cees'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cees.urls'

WSGI_APPLICATION = 'cees.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #'django.db.backends.sqlite3',
        'NAME': 'ceesdb', #os.path.join(BASE_DIR, 'db.sqlite3'),
        'HOST':'127.0.0.1',
        'PORT':3306,
        'USER':'root',
        'PASSWORD':'Superuser'
    }
}

#Logging.
LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : False,
    'formatters' : {
        'simple' : {
            'format' : '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt' : '%d/%b/%Y %H:%M:%S'
        },
        'verbose' : {
            'format' : '[%(asctime)s] %(levelname)s [%(name)s : %(lineno)s] %(message)s',
            'datefmt' : '%d/%b/%Y %H:%M:%S'
        }
    },
    'handlers' : {
        'console' : {
            'level' : 'DEBUG',
            'class' : 'logging.StreamHandler',
            'formatter' : 'simple'
        },

        'app_file' : {
            'level' : 'INFO',
            'class' : 'logging.FileHandler',
            'filename' : 'logs/application.log',
            'formatter' : 'verbose'
        },

        'db_file' : {
            'level' : 'DEBUG',
            'class' : 'logging.FileHandler',
            'filename' : 'logs/database.log',
            'formatter' : 'verbose'
        }
    },
    'loggers' : {

        'django.request' : {
            'handlers' : ['console'],
            'level' : 'DEBUG',
            'propagate' : True
        },

        'django.db' : {
            'handlers' : ['db_file'],
            'level' : 'DEBUG',
            'propagate' : True
        },

        'cees.app' : {
            'handlers' : ['app_file'],
            'level' : 'INFO',
            'propagate' : True
        }

    }

}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Swagger. API doc.

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
