from django.contrib.gis.db import models
from graph.models import StatisticsFormVariable


class Departamento(StatisticsFormVariable):
        numero = models.PositiveIntegerField(primary_key=True, help_text="Introduzca el numero del Departamento")
	geom = models.GeometryField(srid=26716,null=True,blank=True)
	objects = models.GeoManager()


	def generate_map(self):
		qs= self.municipios.all()
		polygon=qs.unionagg()
		return polygon


	def geosave(self, force_insert=False, force_update=False):
		if self.geom== None:
			try:
				print "Starting geom calculation for "+self.nombre+"!"
				self.geom=self.generate_map()
		                self.save(force_insert,force_update)
				print self.nombre+" saved!"
			except:
				print "Geom calculation unsuccesful!"

	def __unicode__(self):
		return str(self.numero)+" "+self.nombre

class Municipio(StatisticsFormVariable):
        numero = models.PositiveIntegerField(primary_key=True, help_text="Indroduzca el numero de Municipio")
	departamento = models.ForeignKey(Departamento,related_name='municipios')	
	geom = models.GeometryField(srid=26716,null=True,blank=True)
	objects = models.GeoManager()

	def __unicode__(self):
		return str(self.numero)+" "+self.nombre


	def generate_map(self):
		qs= self.related_mun_maps.all()
		polygon=qs.unionagg()
		return polygon


	def geosave(self, force_insert=False, force_update=False):
		if self.geom== None:
			try:
				print "Starting geom calculation for "+self.nombre+"!"
				self.geom=self.generate_map()
		                self.save(force_insert,force_update)
				print self.nombre+" saved!"
			except:
				print "Geom calculation unsuccesful!"
                super(Departamento, self).save(force_insert,force_update)


class mun98nic(models.Model):
	area = models.FloatField()
	perimeter = models.FloatField()
	mun98nic_field = models.FloatField()
	mun98nic_i = models.FloatField()
	munic_id = models.FloatField()
	nmunic = models.CharField(max_length=25)
	ndepto = models.CharField(max_length=25)
	departamen = models.IntegerField()
	areasig = models.FloatField()
	p_urban = models.FloatField()
	p_rural = models.FloatField()
	habitantes = models.FloatField()
	matriz = models.CharField(max_length=16)
	geom = models.MultiPolygonField(srid=26716)
	objects = models.GeoManager()

# Auto-generated `LayerMapping` dictionary for mun98nic model
mun98nic_mapping = {
    'area' : 'AREA',
    'perimeter' : 'PERIMETER',
    'mun98nic_field' : 'MUN98NIC_',
    'mun98nic_i' : 'MUN98NIC_I',
    'munic_id' : 'MUNIC_ID',
    'nmunic' : 'NMUNIC',
    'ndepto' : 'NDEPTO',
    'departamen' : 'DEPARTAMEN',
    'areasig' : 'AREASIG',
    'p_urban' : 'P_URBAN',
    'p_rural' : 'P_RURAL',
    'habitantes' : 'HABITANTES',
    'matriz' : 'MATRIZ',
    'geom' : 'MULTIPOLYGON',
}

class dep50nic(models.Model):
    area = models.FloatField()
    perimeter = models.FloatField()
    dep50nic_field = models.FloatField()
    dep50nic_i = models.FloatField()
    depto = models.CharField(max_length=35)
    geom = models.MultiPolygonField(srid=26716)
    objects = models.GeoManager()

# Auto-generated `LayerMapping` dictionary for dep50nic model
dep50nic_mapping = {
    'area' : 'AREA',
    'perimeter' : 'PERIMETER',
    'dep50nic_field' : 'DEP50NIC_',
    'dep50nic_i' : 'DEP50NIC_I',
    'depto' : 'DEPTO',
    'geom' : 'MULTIPOLYGON',
}

