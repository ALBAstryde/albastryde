from django.conf.urls.defaults import *
from django.conf import settings




urlpatterns = patterns('biblioteca.views',
    # Example:
    (r'^index/$',  'search'),
    (r'^detalle/(?P<libro>[^/]+)/$',  'detalle'),
    
)
