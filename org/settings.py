"""
Django settings for org project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from org.deployment import *

import os, rsa
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
site_join = lambda rpath: os.path.join(BASE_DIR, rpath).replace('\\','/')

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS = (
	site_join('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.request',
	'django.contrib.auth.context_processors.auth',
	'django.contrib.messages.context_processors.messages',
	# 'django.core.context_processors.debug',
	# 'django.core.context_processors.i18n',
	# 'django.core.context_processors.media',
)

INSTALLED_APPS = (
	'django_admin_bootstrapped.bootstrap3',
	'django_admin_bootstrapped',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'index',
	'products',
	'accounts',
	'blogs',
	'smartcontract',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware'
)

AUTHENTICATION_BACKENDS = (
    'org.rsa_authentication.RSABackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'org.urls'
WSGI_APPLICATION = 'org.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
# USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
	site_join("static"),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'org.standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'org.request': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': site_join('deployment/log/org.request.log'),
            'formatter': 'org.standard',
        },
        'org.database': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': site_join('deployment/log/org.database.log'),
            'formatter': 'org.standard',
        },
        'org.security': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': site_join('deployment/log/org.security.log'),
            'formatter': 'org.standard',
        },
        'org.main': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': site_join('deployment/log/org.main.log'),
            'formatter': 'org.standard',
        },
        'org.lambda': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': site_join('deployment/log/org.lambda.log'),
            'formatter': 'org.standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['org.request'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['org.database'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['org.security'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'org': {
            'handlers': ['org.main'],
            'level': 'WARNING',
            'propagate': False,
        },
        'org.lambda': {
            'handlers': ['org.lambda'],
            'level': 'ERROR',
            'propagate': False,
        },
        'org.security': {
            'handlers': ['org.security'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# Adjust with caution #bits, on which these depend:
#   static/js/utils.js: function encrypt(m)
#   org/rsa_authentication.py: def decrypt(crypto, priv_key)
RSA_LOGIN_KEY = rsa.newkeys(300)
