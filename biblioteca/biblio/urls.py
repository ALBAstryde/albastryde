from django.conf.urls.defaults import *
from django.conf import settings




urlpatterns = patterns('biblio.views',
    # Example:
    (r'^index/$',  'search'),
    (r'^detalle/(?P<libro>[^/]+)/$',  'detalle'),
    
)
