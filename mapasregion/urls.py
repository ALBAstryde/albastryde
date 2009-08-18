from django.conf.urls.defaults import *
from django.conf import settings
from mapa.models import Mapa
from mapa.views import lista_mapa

urlpatterns = patterns('mapa.views',
      (r'^mapa/lista/tipo/(?P<t>[^/]+)', 'lista_mapa'),
      (r'^mapa/lista/region/(?P<r>[^/]+)', 'lista_mapa_region'),
      (r'^mapa/$', 'index_mapa'),
           
 
)
