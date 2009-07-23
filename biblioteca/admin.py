from django.contrib import admin
from models import Autor, Editorial, Documento, PalabraClave
from django import forms

#class PalabraClaveInline(admin.TabularInline):
#	model = PalabraClave

class DocumentoAdmin(admin.ModelAdmin):
	list_display = ('nombre','autor','fecha_anadido','attachment')
	list_filter = ('autor','fecha_anadido','organizacion')
	ordering = ('fecha_anadido',)
	search_fields = ('nombre', 'attachment','autor')

admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(PalabraClave)
admin.site.register(Documento, DocumentoAdmin)
