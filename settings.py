# -*- coding: utf-8 -*-

from local_settings import *
LOGIN_REDIRECT_URL="/"
COMPRESS_JS_FILTERS=('compress.filters.jsmin.JSMinFilter','compress.filters.yui.YUICompressorFilter',)
COMPRESS_CSS_FILTERS=('compress.filters.csstidy.CSSTidyFilter','compress.filters.yui.YUICompressorFilter',)


TEMPLATE_DEBUG = DEBUG
AUTH_PROFILE_MODULE = "profiles.UserProfile"
DEFAULT_CHARSET = 'utf-8'
MANAGERS = ADMINS
DATABASE_ENGINE = 'postgresql_psycopg2'     
SEARCH_ENGINE = 'postgresql' 
ACCOUNT_ACTIVATION_DAYS = 7
SITE_ID = 1
USE_I18N = True
ADMIN_MEDIA_PREFIX = '/media/admin/'

COMPRESS_CSS = {
	'all': {
        	'source_filenames': ('css/base-style.css', 'css/'+SITE_THEME+'/style.css'),
        	'output_filename': 'css/'+SITE_THEME+'/all_compressed.css',
	}
}

COMPRESS_JS = {
	'all': {
        	'source_filenames': (
			'javascript/jquery.js',
			'javascript/'+SITE_LANGUAGE+'.js',             
			'javascript/translator.js',
			'javascript/jquery.badBrowser.js',
			'javascript/date.js',
			'javascript/jquery.dimensions.js',
			'javascript/jquery.form.js',
			'javascript/jquery.ui.js',
			'javascript/jquery.flot.js',
			'javascript/graph_drawer.js',
			'javascript/statistics_form.js',
			'javascript/site_setup.js'
		),
        	'output_filename': 'javascript/all_'+SITE_LANGUAGE+'_compressed.js',
	}
}



TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth', 
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n',
    'context_processors.site_theme',
    'context_processors.site_language',
    'context_processors.menu_list',
    'context_processors.compress',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
MEDIA_ROOT = SITE_ROOT+'/media/'
MEDIA_URL = '/media/'
TEMPLATE_DIRS = (
    SITE_ROOT+"/templates",
)
ROOT_URLCONF = 'urls'
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_evolution',
    'compress',
    'albastryde.wiki',
    'albastryde.precios',
    'albastryde.graph',
    'albastryde.valuta',
    'django.contrib.gis',
    'albastryde.admin_bulk_add',
#    'albastryde.mapa',
    'albastryde.lugar',
#    'albastryde.climate',
    'albastryde.cosecha',
    'albastryde.lluvia',
    'django.contrib.comments',
    'albastryde.ajax_comments',
    'albastryde.registration',
    'albastryde.profiles',
)
