from django.contrib import admin
from models import Cooperativa, Persona, Producto, Departamento, Proyecto, Variedad, Beneficiario
#from proyectos.ajax_select import make_ajax_form
from forms import beneForm

class ListarBeneAdmin(admin.ModelAdmin):
	list_filter = ('nombre',)


admin.site.register(Cooperativa)
admin.site.register(Persona, ListarBeneAdmin)
admin.site.register(Producto)
admin.site.register(Departamento)
admin.site.register(Proyecto)
admin.site.register(Variedad)
admin.site.register(Beneficiario)
