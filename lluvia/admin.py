from lluvia.models import EstacionDeLluvia, Prueba

#from django.contrib import admin
import admin_extensions as admin

admin.site.register(EstacionDeLluvia)

class LLuviaPruebaAdmin(admin.ModelAdmin):
        list_display   = ('estacion','fecha','__unicode__')
#        date_hierarchy = 'fecha'
        list_filter    = ('estacion', 'fecha')
        ordering       = ('fecha','estacion')



admin.site.register(Prueba,LLuviaPruebaAdmin)


