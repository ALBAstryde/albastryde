from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('biblioteca.views',
    (r'^$',  'index'),
    (r'^palabra_clave/(?P<pk>[^/]+)/$', 'palabra_clave'),
    (r'^detalle/(?P<libro>[^/]+)/$',  'detalle'),    
)
