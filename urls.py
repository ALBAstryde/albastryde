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

def gotowiki(request):
	return HttpResponseRedirect("/wiki/"+settings.WIKI_STARTPAGE)

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^wiki/searchresults/$', 'albastryde.wiki.views.search_page'),
    (r'^wiki/list/$', 'albastryde.wiki.views.list_page'),
    (r'^wiki/(?P<page_name>[^/]+)/$', 'albastryde.wiki.views.view_page'),
    (r'^$', gotowiki),
    (r'^wiki/$', gotowiki),
    (r'^estadisticas/(?P<query_string>.+)$', 'albastryde.graph.views.show_graph'),
    (r'^estadisticas/$', 'albastryde.graph.views.show_form'),
    (r'^comments/', include('django.contrib.comments.urls')),
     (r'^ajax/', include('albastryde.ajax_comments.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),
)
