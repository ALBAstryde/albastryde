from django.conf.urls.defaults import *
from django.conf import settings
from mapasregion.models import Mapa
from mapasregion.views import lista_mapa

urlpatterns = patterns('mapasregion.views',
      (r'^lista/tipo/(?P<t>[^/]+)', 'lista_mapa'),
      (r'^lista/region/(?P<r>[^/]+)', 'lista_mapa_region'),
      (r'^$', 'index_mapa'),
           
 
)
