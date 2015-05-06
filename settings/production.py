# -*- coding: utf-8 -*-
"""
Production Configurations

- Use djangosecure
- Use Amazon's S3 for storing static files and uploaded media
- Use MEMCACHIER on Heroku
"""

import os

from configurations import values

from .common import Common


class Production(Common):

    # This ensures that Django will be able to detect a secure connection
    # properly on Heroku.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    # END INSTALLED_APPS

    # SECRET KEY
    SECRET_KEY = values.SecretValue()
    # END SECRET KEY

    # django-secure
    INSTALLED_APPS += (
        'djrill',
        'opbeat.contrib.django',
        'djangosecure',
    )

    # MIDDLEWARE CONFIGURATION
    MIDDLEWARE_CLASSES = (
        # Make sure djangosecure.middleware.SecurityMiddleware is listed first
        'djangosecure.middleware.SecurityMiddleware',
        'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    )

    MIDDLEWARE_CLASSES += Common.MIDDLEWARE_CLASSES
    # END MIDDLEWARE CONFIGURATION

    # set this to 60 seconds and then to 518400 when you can prove it works
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SESSION_COOKIE_SECURE = values.BooleanValue(False)
    SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    # end django-secure

    # SITE CONFIGURATION
    # Hosts/domain names that are valid for this site
    # See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    # END SITE CONFIGURATION

    INSTALLED_APPS += ("gunicorn", )

    # STORAGE CONFIGURATION
    # See: http://django-storages.readthedocs.org/en/latest/index.html
    INSTALLED_APPS += (
        'storages',
    )

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = values.SecretValue()
    AWS_SECRET_ACCESS_KEY = values.SecretValue()
    AWS_STORAGE_BUCKET_NAME = values.SecretValue()
    AWS_AUTO_CREATE_BUCKET = True
    AWS_QUERYSTRING_AUTH = False

    # See: https://github.com/antonagestam/collectfast
    # For Django 1.7+, 'collectfast' should come before 'django.contrib.staticfiles'
    AWS_PRELOAD_METADATA = True
    INSTALLED_APPS = ('collectfast', ) + INSTALLED_APPS

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIRY = 60 * 60 * 24 * 7
    AWS_HEADERS = {
        'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (
            AWS_EXPIRY, AWS_EXPIRY)
    }
    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html
    try:
        from boto.s3.connection import OrdinaryCallingFormat
        AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
    except ImportError:
        pass

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    # END STORAGE CONFIGURATION

    # EMAIL
    SERVER_EMAIL = DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
    MANDRILL_API_KEY = os.environ.get("MANDRILL_API_KEY")
    # END EMAIL

    # TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )
    # END TEMPLATE CONFIGURATION

    # CACHING
    # Only do this here because thanks to django-pylibmc-sasl and pylibmc
    # memcacheify is painful to install on windows.
    try:
        # See: https://github.com/rdegges/django-heroku-memcacheify
        from memcacheify import memcacheify
        CACHES = memcacheify()
    except ImportError:
        CACHES = values.CacheURLValue(default="memcached://127.0.0.1:11211")
    # END CACHING

    # ====
    # SOSH
    # ====
    SOSH = {
        "google": {
            "CLIENT_ID": os.environ.get('SOSH_GOOGLE_CLIENT_ID'),
            "CLIENT_SECRET": os.environ.get("SOSH_GOOGLE_SECRET"),
            "CALLBACK_URL": "http://pants.party/auth/google/"
        },
        "twitter": {
            "CONSUMER_KEY": os.environ.get('SOSH_TWITTER_CONSUMER_KEY'),
            "CONSUMER_SECRET": os.environ.get("SOSH_TWITTER_SECRET"),
            "CALLBACK_URL": "http://pants.party/auth/twitter/"
        },
        "facebook": {
            "CLIENT_SECRET": os.environ.get("SOSH_FACEBOOK_SECRET")
        }
    }

    # ======
    # opbeat
    # ======
    OPBEAT = {
        "ORGANIZATION_ID": os.environ.get('OPBEAT_ORGANIZATION_ID'),
        "APP_ID": os.environ.get('OPBEAT_APP_ID'),
        "SECRET_TOKEN": os.environ.get('OPBEAT_SECRET_TOKEN'),
        "DEBUG": True
    }
