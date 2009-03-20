import os, sys
import SITE_URL from local_settings

sys.path.append(SITE_URL)
sys.path.append(SITE_URL+'/albastryde')
sys.path.append(SITE_URL+'/albastryde/wiki')
os.environ['DJANGO_SETTINGS_MODULE'] = 'albastryde.settings'
os.environ['MPLCONFIGDIR'] = topdir+"/albastryde/media/cache/" 
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
