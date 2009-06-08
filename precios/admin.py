from precios.models import Producto, Mercado, Prueba, Medida
#from django.contrib import admin
import admin_extensions as admin

admin.site.register(Producto)
admin.site.register(Mercado)
admin.site.register(Medida)


class PruebaAdmin(admin.ModelAdmin):
	list_display   = ('es_aprobado','fecha','mercado', 'producto', '__unicode__')
	date_hierarchy = 'fecha'
        list_filter    = ('mercado', 'producto','es_aprobado','creado_por')
        #filter_vertical    = ('mercado', 'producto')
        ordering       = ('fecha','producto','mercado')
#	if (request.user.has_perm(Prueba.can_approve)):
#		autopopulate = { 
#			'created_by': lambda request, instance: request.user, 'is_approved' : True
#		}
#	else:
#	if 1:
	autofilter = {'creado_por': lambda request: request.user }
#		autopopulate = { 'created_by': lambda request: request.user}
#		autopopulate = { 'created_by': lambda request, instance: request.user, 'updated_by': lambda request, instance: request.user, 'is_approved' : False }
#		autohide = ['created_by']

	def save_model(self, request, obj, form, change):
		obj.actualizado_por = request.user
#		if (request.user.has_perm('Prueba.can_approve')):
#			obj.is_approved = True
#		else:
#			obj.is_approved = False
        	obj.save()
	

admin.site.register(Prueba, PruebaAdmin)

