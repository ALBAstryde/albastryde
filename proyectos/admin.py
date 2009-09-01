from django.contrib import admin
from models import Cooperativa, Persona, Producto, Departamento, Proyecto, Variedad, Beneficiario

class ListarBeneAdmin(admin.ModelAdmin):
	list_filter = ('nombre',)

admin.site.register(Cooperativa)
admin.site.register(Persona, ListarBeneAdmin)
admin.site.register(Proyecto)
admin.site.register(Variedad)
admin.site.register(Beneficiario)
