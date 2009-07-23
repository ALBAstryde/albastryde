#from django.conf.urls.defaults import *
from coffin.conf.urls.defaults import * 
from django.http import HttpResponseRedirect
from django.conf import settings
#from django.contrib.comments.models import Comment

# Uncomment the next two lines to enable the admin:
#import admin
#from django.contrib import admin
from django.contrib.gis import admin
admin.autodiscover()

#import django_cron
#django_cron.autodiscover()

def gotowiki(request):
	return HttpResponseRedirect("/wiki/"+settings.WIKI_STARTPAGE)

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/precios/prueba/bulk_add/$', 'albastryde.admin_bulk_add.views.precios'),
    (r'^admin/precios/prueba/bulk_add/(?P<mercado>[^/]+)/(?P<ano>[^/]+)/(?P<mes>[^/]+)/(?P<dia>[^/]+)/$', 'albastryde.admin_bulk_add.views.precios'),
    (r'^admin/lluvia/prueba/bulk_add/$', 'albastryde.admin_bulk_add.views.lluvia'),
    (r'^admin/lluvia/prueba/bulk_add/(?P<estacion_de_lluvia>[^/]+)/(?P<ano>[^/]+)/(?P<mes>[^/]+)/$', 'albastryde.admin_bulk_add.views.lluvia'),
    (r'^admin/(.*)', admin.site.root),
    (r'^busqueda/(?P<search_term>[^/]+)/$', 'albastryde.wiki.views.search_page'),
    (r'^busqueda/$', 'albastryde.wiki.views.search_page'),
    (r'^busqueda_html/$', 'albastryde.wiki.views.search_page_html'),
    (r'^list/$', 'albastryde.wiki.views.list_page'),
    (r'^list/(?P<tag_name>[^/]+)/$', 'albastryde.wiki.views.list_page'),
    (r'^wiki/(?P<page_name>[^/]+)/$', 'albastryde.wiki.views.view_page'),
    (r'^$', gotowiki),
    (r'^wiki/$', gotowiki),
    (r'^estadisticas/(?P<query_string>.+)$', 'albastryde.graph.views.show_graph'),
    (r'^estadisticas/$', 'albastryde.graph.views.show_form'),
    (r'^estadisticas_(?P<statistics_variable>[^/]+)/$', 'albastryde.graph.views.show_form'),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^ajax/', include('albastryde.ajax_comments.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),
    (r'^biblioteca/', include('biblioteca.urls')),
    (r'^bibliotecasearch/$', 'biblio.views.search'),
)
