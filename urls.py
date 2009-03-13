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
    # Example:
#   (r'^albastryde/', include('albastryde.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^wiki/searchresults/$', 'albastryde.wiki.views.search_page'),
    (r'^wiki/list/$', 'albastryde.wiki.views.list_page'),
    (r'^wiki/(?P<page_name>[^/]+)/$', 'albastryde.wiki.views.view_page'),
    (r'^$', gotowiki),
    (r'^wiki/$', gotowiki),
#    (r'^wiki/(?P<page_name>[^/]+)/edit/$', 'albastryde.wiki.views.edit_page'),
#    (r'^wiki/(?P<page_name>[^/]+)/save/$', 'albastryde.wiki.views.save_page'),
    (r'^js/wiki/searchresults/$', 'albastryde.wiki.views.search_page',{'javascript':True}),
    (r'^js/wiki/list/$', 'albastryde.wiki.views.list_page',{'javascript':True}),
    (r'^js/wiki/(?P<page_name>[^/]+)/$', 'albastryde.wiki.views.view_page',{'javascript':True}),
    (r'^js$', gotowiki),
    (r'^js/wiki/$', gotowiki),
#    (r'^js/wiki/(?P<page_name>[^/]+)/edit/$', 'albastryde.wiki.views.edit_page',{'javascript':True}),
#    (r'^js/wiki/(?P<page_name>[^/]+)/save/$', 'albastryde.wiki.views.save_page',{'javascript':True}),
    (r'^estadisticas/$', 'albastryde.graph.views.get_js_graph'),
    (r'^js/estadisticas/$', 'albastryde.graph.views.get_js_graph',{'javascript':True}),
    (r'^comments/', include('django.contrib.comments.urls')),
     (r'^ajax/', include('albastryde.ajax_comments.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),
)
