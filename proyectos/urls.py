from django.conf.urls.defaults import *
from os import path as os_path
from django.conf import settings
from proyectos.views import *

# esto de aqui solo es prueba para ver algunas salidas ya te mande a tu correo lo que se requiere hacer como salidas
urlpatterns = patterns('proyectos.views',
   (r'^proyecto/$',  ConsulForm),
   (r'^persona/$',  Beneficiario),
   (r'^detalle/$',  ConsulProyecto),
   
 )
