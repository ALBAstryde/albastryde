from climate.models import Temperatura, Precipitation, Canicula, TierraPerfil, Topografia, Erosion


def run():
	a=Temperatura.objects.all()
	b=Precipitation.objects.all()
	c=TierraPerfil.objects.all()
	d=Topografia.objects.all()
	e=Erosion.objects.all()
	
	for i in a:
	        i.geom_save(force_update=True)

	for i in b:
	        i.geom_save(force_update=True)

	for i in c:
	        i.geom_save(force_update=True)

	for i in d:
	        i.geom_save(force_update=True)

	for i in e:
        	i.geom_save(force_update=True)

	f=Canicula.objects.all()
	for i in f:
        	i.geom_save(force_update=True)
