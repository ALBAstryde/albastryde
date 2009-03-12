from climate.models import Temperatura, Precipitation, Canicula, TierraPerfil, Topografia, Erosion,Textura

from django.contrib.gis import admin

admin.site.register(Temperatura, admin.GeoModelAdmin)
admin.site.register(Precipitation, admin.GeoModelAdmin)
admin.site.register(Topografia, admin.GeoModelAdmin)
admin.site.register(Erosion, admin.GeoModelAdmin)
admin.site.register(Canicula, admin.GeoModelAdmin)
admin.site.register(Textura)
admin.site.register(TierraPerfil, admin.GeoModelAdmin)


