# -*- encoding: utf-8 -*-

import datetime
from django.db import models
#from lugar.models import Departamento, Municipio
#from graph.models import StatisticsFormVariable

#class Producto(StatisticsFormVariable):
#	pass

#PRODUCTOS_CHOICES=((1,"Maiz"),(2,"Frijol"),(3,"Arroz"),(4,"Sorgo Industrial"),(5,"Sorgo millon"),(6,"Sorgo blanco"))

class ProductoCosecha(models.Model):
		nombres = models.CharField(max_length=50, null=True, blank=True)
		numero_producto = models.PositiveIntegerField(primary_key=True)
		def __unicode__(self):
    			return self.nombres
		class Meta:
    			ordering = ['nombres']

ANOS_CHOICES=[]

for i in range (datetime.date.today().year+1,1999,-1):
          ANOS_CHOICES.append((i,str(i)+'-'+str(i+1)))

TIEMPO_CHOICES=((1,"primera"),(2,"postrera"),(3,"apante"))

class Departamentos(models.Model):
	nombre = models.CharField(max_length=60, help_text="Introduzca el nombre del departamento")
	numero_departamento = models.PositiveIntegerField(primary_key=True, help_text="Introduzca el numero del Departamento")
	def __unicode__(self):
		return str(self.numero_departamento) + " " + self.nombre

	class Meta:
	     ordering = ["nombre"]

class Municipio(models.Model):
	nombre = models.CharField(max_length=60, help_text="Ingrese el nombre del municipio")
	numero_municipio = models.PositiveIntegerField(primary_key=True, help_text="Indrouzca el numero de Municipio")
	numero_departamento = models.ForeignKey(Departamentos, null=True, blank=True)
	def __unicode__(self):
		return str(self.numero_municipio) + " " + self.nombre
	class Meta:
              ordering = ["nombre"]

class Cosecha(models.Model):
        municipio=models.ForeignKey(Municipio)
	anos=models.PositiveIntegerField(choices=ANOS_CHOICES)
	tiempo=models.IntegerField(choices=TIEMPO_CHOICES)
	producto=models.ForeignKey(ProductoCosecha)
        area_estimada=models.IntegerField()
        producto_estimado=models.IntegerField()
        area_sembrada=models.IntegerField()
        area_cosechada=models.IntegerField()
	producto_obtenido=models.IntegerField()
#	def __unicode__(self):
#		return self.producto
