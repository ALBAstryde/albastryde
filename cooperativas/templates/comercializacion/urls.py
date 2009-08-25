from django.conf.urls.defaults import *
from albastryde.cooperativas.models import Cooperativa, Detallecoop

urlpatterns = patterns('albastryde.lugar.views',
	(r'^departamento/$', 'comeindex'),
	(r'^cooperativa/(?P<mun_id>\d+)/$', 'coopmun'),
	(r'^ver/(?P<deta_id>\d+)/$', 'verdetalle'),
	(r'^detallec/(?P<p_id>\d+)/$', 'detacompleto'),
)
