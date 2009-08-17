from django.contrib import admin
from models import Autor, Editorial, Documento, PalabraClave
from django import forms

from ajax_filtered_fields.forms import AjaxManyToManyField
from django.conf import settings

#class PalabraClaveInline(admin.TabularInline):
#	model = PalabraClave

class DocumentoAdmin(admin.ModelAdmin):
	list_display = ('nombre','autor','fecha_anadido','attachment')
	list_filter = ('autor','fecha_anadido','organizacion')
	ordering = ('fecha_anadido',)
	search_fields = ('nombre', 'attachment','autor')
        # lookups explained below
        related_objects = AjaxManyToManyField(PalabraClave, (('all stuff', {}),))

#        class Meta:
#            model = Model

        class Media:
		js = (
                	settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
                	settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js",
                	'/media/javascript/jquery.js',
                	'/media/ajax_filtered_fields/ajax_filtered_fields.js',
		)


admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(PalabraClave)
admin.site.register(Documento, DocumentoAdmin)
