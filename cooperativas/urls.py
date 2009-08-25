from django.conf.urls.defaults import *
from cooperativas.models import Cooperativa, Detallecoop



urlpatterns = patterns('cooperativas.views',
	(r'^$', 'index'),
	(r'^listar/(?P<listar_id>\d+)/$', 'cooperativar'),
	(r'^detalle/(?P<deta_id>\d+)/$', 'detallelistar'),
	(r'^comercializacion/$', 'comercio'),
	(r'^comercia/$', 'comerciobruto'),
	# vistas de cooperativas desde lugar vienen
	(r'^departamento/$', 'comeindex'),
	(r'^cooperativa/(?P<mun_id>\d+)/$', 'coopmun'),
	(r'^ver/(?P<deta_id>\d+)/$', 'verdetalle'),
	(r'^detallec/(?P<p_id>\d+)/$', 'detacompleto'),
)

