from lugar.models import Departamento, Municipio
from lugar.models import dep50nic,mun98nic
#from django.contrib import admin
#import admin_extensions as admin
#from wiki.forms import PaginaForm

from django.contrib.gis import admin
#from models import zoninac_50000

#admin.site.register(zoninac_50000, admin.GeoModelAdmin)

#admin.site.register(Pagina)
admin.site.register(Departamento, admin.GeoModelAdmin)
admin.site.register(Municipio, admin.GeoModelAdmin)

admin.site.register(dep50nic, admin.GeoModelAdmin)
admin.site.register(mun98nic, admin.GeoModelAdmin)


