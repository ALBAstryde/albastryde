from django.contrib import admin
from mapa.models import Mapa, Tipo

class MapaAdmin(admin.ModelAdmin):
	list_display = ['ano','region','tipo']
	list_filter = ['region']
	
class TipoAdmin(admin.ModelAdmin):
	list_display = ['nombre']
     
admin.site.register(Mapa, MapaAdmin)
admin.site.register(Tipo, TipoAdmin)

