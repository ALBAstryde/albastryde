# -*- encoding: utf-8 -*-

import datetime
from django.db import models
from lugar.models import Departamento, Municipio
from graph.models import StatisticsFormVariable

class Producto(StatisticsFormVariable):
	pass

ANOS_CHOICES=[]

for i in range (datetime.date.today().year,1999,-1):
          ANOS_CHOICES.append((i,str(i)+'-'+str(i+1)))

TIEMPO_CHOICES=((1,"primera"),(2,"postrera"),(3,"apante"))

class Cosecha(models.Model):
        municipio=models.ForeignKey(Municipio)
	ano=models.PositiveIntegerField(choices=ANOS_CHOICES,verbose_name='año')
	tiempo=models.IntegerField(choices=TIEMPO_CHOICES)
	producto=models.ForeignKey(Producto)
        area_estimada=models.IntegerField()
        producto_estimado=models.IntegerField()
        area_sembrada=models.IntegerField()
        area_cosechada=models.IntegerField()
	producto_obtenido=models.IntegerField()

	def ano_str(self):
		return str(self.ano)+'-'+str(self.ano+1)

	def tiempo_str(self):
		if self.tiempo==1:
			return "primera"
		elif self.tiempo==2:
			return "postrera"
		elif self.tiempo==3:
			return "apante"
		else:
			return None

	def rendimiento_estimado(self):
		return self.producto_estimado/self.area_estimada

	def rendimiento_obtenido(self):
		return self.producto_obtenido/self.area_cosechada

	def area_perdida(self):
		return self.area_sembrada-self.area_cosechada

	def area_miscalculada(self):
		return self.area_estimada-self.area_sembrada

	def producto_miscalculado(self):
		return self.producto_estimado-self.producto_obtenido

	def __unicode__(self):
		return str(self.producto) + " en " + str(self.municipio) + ", " + str(self.municipio.departamento) + " ("+ self.tiempo_str() + " " + self.ano_str() + ")"
