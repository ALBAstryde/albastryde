from django.conf.urls.defaults import *
from os import path as os_path
from django.conf import settings
from proyecto.views import *

urlpatterns = patterns('proyecto.views',
   (r'^proyecto/$',  ConsulForm),
   (r'^persona/$',  Benefi),
   
 )
