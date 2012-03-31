from settings_base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # > createdb -T template_postgis cas_food
        # > psql
        # # create user cas_food with password 'muppet';
        # # grant all privileges on database cas_food to cas_food;

        'ENGINE': 'django.contrib.gis.db.backends.postgis', 
        'NAME': 'cas_food',                      
        'USER': 'cas_food',                      
        'PASSWORD': 'muppet',                  
        'HOST': 'localhost',                      
        'PORT': '',                      
    }
}

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache',
    }
}

# enter your app id here
YAHOO_APP_ID = 'ENTER-YAHOO-APP-ID-HERE'

# enter a secret key
SECRET_KEY = 'ENTER-KEY-HERE'

