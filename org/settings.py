"""
Django settings for org project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from deployment import *

import os
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

ROOT_URLCONF = 'org.urls'
WSGI_APPLICATION = 'org.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
	site_join("static"),
)
