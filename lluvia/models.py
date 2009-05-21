from django.db import models
from graph.models import StatisticsFormVariable
from lugar.models import Municipio

REGION_CHOICES=[('RAAN','RAAN'),('RAAS','RAAS'),('I','Region I'),('II','Region II'),('III','Region III'),('IV','Region IV'),('V','Region V'),('VI','Region VI'),('None','Quien sabe?')]


class EstacionDeLluvia(StatisticsFormVariable):
	numero = models.IntegerField(primary_key=True)
	municipio = models.ForeignKey(Municipio,blank=True,null=True)
	region = models.CharField(max_length=4,choices=REGION_CHOICES)	

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name_plural='estaciones de lluvia'

class Prueba(models.Model):
	estacion = models.ForeignKey(EstacionDeLluvia)
	milimetros_de_lluvia=models.DecimalField(decimal_places=1,max_digits=4)
	fecha = models.DateField()

	def __unicode__(self):
		return str(self.milimetros_de_lluvia)
