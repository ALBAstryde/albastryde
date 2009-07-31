from django.contrib import admin
from models import Cooperativa, Persona, Producto, Departamento, Proyecto, Variedad, Beneficiario

class BeneAdmin(admin.ModelAdmin):
	list_filter = ('nombre',)

admin.site.register(Cooperativa)
admin.site.register(Persona, BeneAdmin)
admin.site.register(Producto)
admin.site.register(Departamento)
admin.site.register(Proyecto)
admin.site.register(Variedad)
admin.site.register(Beneficiario)
