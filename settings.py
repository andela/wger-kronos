#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wger.settings_global import *
import os

# Use 'DEBUG = True' to get more details for server errors
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True
# TEMPLATE_LOADERS = TEMPLATES[0]['OPTIONS']['loaders']

ADMINS = (
    ('Your name', 'your_email@example.com'),
)
MANAGERS = ADMINS


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': '/Users/allanguwatudde/Desktop/TTL/wger/database.sqlite',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': '5432',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^p&2ga&(q@98hn$)2c!ecn9=29!ao36k#o=(84#wn04k4c+k4a'

# Your reCaptcha keys
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True

# The site's URL (e.g. http://www.my-local-gym.com or http://localhost:8000)
# This is needed for uploaded files and images (exercise images, etc.) to be
# properly served.
SITE_URL = 'http://localhost:8000'

# Path to uploaded files
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '/Users/allanguwatudde/.local/share/wger/media'
MEDIA_URL = '/media/'

# Allow all hosts to access the application. Change if used in production.
ALLOWED_HOSTS = '*'

# This might be a good idea if you setup memcached
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Configure a real backend in production
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Sender address used for sent emails
WGER_SETTINGS['EMAIL_FROM'] = 'wger Workout Manager <wger@example.com>'

# Your twitter handle, if you have one for this instance.
# WGER_SETTINGS['TWITTER'] = ''

PROJECT_ROOT = os.path.join(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
