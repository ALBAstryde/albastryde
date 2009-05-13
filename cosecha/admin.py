from cosecha.models import Cosecha, Producto
from django.contrib import admin
#import admin_extensions as admin

class PmostrarAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

admin.site.register(Cosecha)
admin.site.register(Producto, PmostrarAdmin)
