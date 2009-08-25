from django.conf.urls.defaults import *
from cooperativas.models import Cooperativa, Detallecoop



urlpatterns = patterns('cooperativas.views',
	(r'^$', 'index'),
	(r'^listar/(?P<listar_id>\d+)/$', 'cooperativar'),
	(r'^detalle/(?P<deta_id>\d+)/$', 'detallelistar'),
)

