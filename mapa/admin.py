from django.contrib.gis import admin
from models import zoninac_50000, zones

admin.site.register(zoninac_50000, admin.GeoModelAdmin)
admin.site.register(zones, admin.GeoModelAdmin)

