from django.conf.urls.defaults import *
from os import path as os_path
from django.conf import settings
#from biblio.views import search

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^biblioteca/', include('biblioteca.foo.urls')),
	(r'^biblio/', include('biblio.urls')),
	(r'^$', 'biblio.views.search'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(.*)$', 'django.views.static.serve', {'document_root': os_path.join(settings.MEDIA_ROOT)}),
	)

