# -*- encoding: utf-8 -*-
from django.contrib import admin
from cooperativas.models import  Ecp, Cooperativa, Detallecoop, Comercializacion, Producto

class ProductoAdmin(admin.ModelAdmin):
	list_display = ['nombre']

class EcpAdmin(admin.ModelAdmin):
	list_display = ['nombre']

class CoopAdmin(admin.ModelAdmin):
	list_display = ['ecp','nombre_resumido','msnm','municipio','fecha_constitucion']
	list_filter = ['municipio']
	
class DetalleAdmin(admin.ModelAdmin):
	list_display = ['cooperativa','mem_hombre','mem_mujer','mem_total','ben_hombre','ben_mujer','ben_total']
	list_filter = ['cooperativa']
	
class ComerAdmin(admin.ModelAdmin):
	list_display = ['ciclo','cooperativa','producto','area','produccion','rendimiento','exportacion','precio_expt','certificacion']
	#list_filter = ['cooperativa']

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Ecp, EcpAdmin)
admin.site.register(Cooperativa, CoopAdmin)
admin.site.register(Detallecoop, DetalleAdmin)
admin.site.register(Comercializacion, ComerAdmin)




