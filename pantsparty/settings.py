""",
Django settings for pantsparty project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y3$3^m#sozw8zumn$d=n@hockz(e9k#hov@!-1ow0n@k2=(hm4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

STATIC_PATH = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    STATIC_PATH,
)

TEMPLATE_DIRS = (
    BASE_DIR + "/templates/",
)

ALLOWED_HOSTS = []

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTH_USER_MODEL = 'ppuser.CustomUser'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'django.contrib.admin.apps.SimpleAdminConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.hubic',
    'allauth.socialaccount.providers.persona',
    'allauth.socialaccount.providers.twitter',

    'blog',
    'djrill',
    'faq',
    'corsheaders',
    'opbeat.contrib.django',
    'ppuser',
    'sosh',
    'subscriptions',
    'textjokes',
    # 'testresp',
)

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
MANDRILL_API_KEY = os.environ.get("MANDRILL_API_KEY")

OPBEAT = { 
    "ORGANIZATION_ID": "5ffb6078bbc54300a78b4593190be7e0",
    "APP_ID": "a0cdfc36c7",
    "SECRET_TOKEN": "%s" % (os.environ.get("OPBEAT_SECRET_TOKEN")),
    "DEBUG": True
}

SOSH = { 
    "google" :{
        "CLIENT_ID": "619194941129-08kmjd2nbt526kqmdhc5sgtkt669j2cg.apps.googleusercontent.com",
        "CLIENT_SECRET": os.environ.get("SOSH_GOOGLE_SECRET"),
        "CALLBACK_URL": "http://pants.party/auth/google/"
    },  
    "twitter" : { 
        "CONSUMER_KEY": "c2WJqCMkG9M39bZcas5cid1ms",
        "CONSUMER_SECRET": os.environ.get("SOSH_TWITTER_SECRET"),
        "CALLBACK_URL": "http://pants.party/auth/twitter/"
    },  
    "facebook" :{
        "CLIENT_SECRET": os.environ.get("SOSH_FACEBOOK_SECRET")
    }   
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pantsparty.urls'

WSGI_APPLICATION = 'pantsparty.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

SITE_ID = 1

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'opbeat': {
            'level': 'WARNING',
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'mysite': {
            'level': 'WARNING',
            'handlers': ['opbeat'],
            'propagate': False,
        },
        'opbeat.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'textjokes': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

try:
    from dev_settings import *
except Exception, e:
    # from prod_settings import *
    # from heroku_settings import *
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] =  dj_database_url.config(default="mysql://root:@localhost:3306/pantsparty")

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    # Static asset configuration
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
