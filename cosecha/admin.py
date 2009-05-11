from cosecha.models import Cosecha, ProductoCosecha, Departamentos, Municipio
from django.contrib import admin
#import admin_extensions as admin

class PmostrarAdmin(admin.ModelAdmin):
	list_display = ('nombres',)

admin.site.register(Cosecha)
admin.site.register(ProductoCosecha, PmostrarAdmin)
admin.site.register(Departamentos)
admin.site.register(Municipio)
