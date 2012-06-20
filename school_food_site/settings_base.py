import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'mobile.middleware.MobileMiddleware',
)

ROOT_URLCONF = 'school_food_site.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)
TEMPLATE_MOBILE_DIR = "mobile"
TEMPLATE_SCREEN_DIR = "screen"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'appmedia',
    'ckeditor',
    'django_jenkins',
    'registration',
    'selectable',
    'south',
    'sorl.thumbnail',

    'accounts',
    'audit',
    'connect',
    'content',
    'feedback',
    'food',
    'getinvolved',
    'glossary',
    'organize',
    'pages',
    'schools',
    'tray',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'food.context_processors.todays_menu',
    'mobile.context_processors.mobile',
)

INTERNAL_IPS = ('127.0.0.1',)

ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

THUMBNAIL_UPSCALE = False

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'kama',
        'toolbar': (
            [ 'Source', '-', 'Bold', 'Italic','Underline','-','RemoveFormat'  ],
            [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ],
            [ 'NumberedList','BulletedList','-','Blockquote','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            [ 'Link','Unlink' ],
            [ 'Image','Flash','Table','SpecialChar' ],
        ),
    },
    'admin': {
        'skin': 'v2',
        'toolbar': 'Full',
    },
}

# apps to be tested by django-jenkins
PROJECT_APPS = (
    'accounts',
    'audit',
    'connect',
    'content',
    'feedback',
    'flatpages',
    'food',
    'getinvolved',
    'glossary',
    'organize',
    'schools',
    'tray',
)

JENKINS_TASKS = (
        'django_jenkins.tasks.with_coverage',
        'django_jenkins.tasks.run_pylint',
        'django_jenkins.tasks.django_tests',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'log_file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'INFO'
    },
}

DEFAULT_GROUP = 'standard users'
