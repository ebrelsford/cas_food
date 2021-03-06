import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
COMPRESS_ROOT = MEDIA_ROOT

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',

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
    # contrib
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd-party
    'appmedia',
    'ckeditor',
    'compressor',
    'django_jenkins',
    'google_analytics',
    'registration',
    'selectable',
    'south',
    'sorl.thumbnail',

    # internal
    'alias',
    'accounts',
    'audit',
    'casfood_comments',
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

TEST_RUNNER="ignoretests.DjangoIgnoreTestSuiteRunner"
IGNORE_TESTS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'appmedia',
    'ckeditor',
    'compressor',
    'django_jenkins',
    'registration',
    'selectable',
    'south',
    'sorl.thumbnail',
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
    'getinvolved.context_processors.promoted_posts',
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
ACTIVE_BOROUGHS = ('Brooklyn', 'Manhattan',)
ACTIVE_SCHOOL_TYPES = (
    'Early Childhood',
    'Elementary',
    'K-8',
)

GOOGLE_ANALYTICS_MODEL = True
