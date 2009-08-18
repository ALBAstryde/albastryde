from django.conf.urls.defaults import *
from cooperativas.models import Cooperativa, Detallecoop

#info = {
#	'queryset': Cooperativa.objects.all(),
	#'queryset': Detallecoop.objects.all(),
#}

#info_dict = {
#	'queryset': Detallecoop.objects.all(),
#}

#urlpatterns = patterns('django.views.generic.list_detail',
#	url(r'^$', 'object_list', info, name='cooperativa-list'),
#	url(R'^(?P<object_id>\d+)/$', 'object_detail', info, name='cooperativa-detail'),
#	url(r'^$', 'object_list', info, name='Detallecoop-list'),
#	url(R'^(?P<object_id>\d+)/$', 'object_detail', info, name='Detallecoop-detail'),
#)

urlpatterns = patterns('cooperativas.views',
	(r'^$', 'index'),
	(r'^listar/(?P<listar_id>\d+)/$', 'cooperativar'),
	(r'^detalle/(?P<deta_id>\d+)/$', 'detallelistar'),
	#(r'^departamento/$', 'comeindex'),
)

