from django.conf.urls.defaults import *
from models import Cooperativa, Detallecoop


urlpatterns = patterns('mapamagfor.cooperativa.views',
	(r'^index/$', 'index'),
	(r'^listar/(?P<listar_id>\d+)/$', 'cooperativar'),
	(r'^detalle/(?P<deta_id>\d+)/$', 'detallelistar'),
	# urls.py de comercializacion
	(r'^comercializacion/$', 'comercio'),
	(r'^comercia/$', 'comerciobruto'),
)

