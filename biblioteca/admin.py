from django.contrib import admin
from models import Autor, Editorial, Documento, PalabraClave


#class PalabraClaveInline(admin.TabularInline):
#	model = PalabraClave

class DocumentoAdmin(admin.ModelAdmin):
	list_display = ('nombre','autor','fecha_anadido','attachment')
	list_filter = ('autor','fecha_anadido','organizacion')
	raw_id_fields = ("palabras_claves",)
#	inlines = [
#		PalabraClaveInline,
#	]
	ordering = ('fecha_anadido',)
	search_fields = ('nombre', 'attachment','autor')

admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Documento, DocumentoAdmin)
