from django.conf.urls.defaults import *
from mapamagfor.cooperativa.models import Cooperativa, Detallecoop

urlpatterns = patterns('mapamagfor.lugar.views',
	(r'^departamento/$', 'comeindex'),
	(r'^cooperativa/(?P<mun_id>\d+)/$', 'coopmun'),
	(r'^ver/(?P<deta_id>\d+)/$', 'verdetalle'),
	(r'^detallec/(?P<p_id>\d+)/$', 'detacompleto'),
)
