from django.db import models

class EstacionDeLluvia(models.Model):
	nombre = models.CharField(max_length=60)
	numero = models.IntegerField(primary_key=True)

	def __unicode__(self):
		return self.nombre


class Prueba(models.Model):
	estacion = models.ForeignKey(EstacionDeLluvia)
	milimetros_de_lluvia=models.DecimalField(decimal_places=1,max_digits=4)
	fecha = models.DateField()

	def __unicode__(self):
		return str(self.milimetros_de_lluvia)
