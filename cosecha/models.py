import datetime
from django.db import models
from lugar.models import Departamento, Municipio
from graph.models import StatisticsFormVariable

class Producto(StatisticsFormVariable):
	pass

ANOS_CHOICES=[]

for i in range (datetime.date.today().year+1,1999,-1):
          ANOS_CHOICES.append((i,str(i)+'-'+str(i+1)))

TIEMPO_CHOICES=((1,"primera"),(2,"postrera"),(3,"apante"))


# Create your models here.
class Cosecha(models.Model):
	departamento=models.ForeignKey(Departamento)
        municipio=models.ForeignKey(Municipio)
	anos=models.PositiveIntegerField(choices=ANOS_CHOICES)
	tiempo=models.IntegerField(choices=TIEMPO_CHOICES)
	producto=models.ForeignKey(Producto)
        area_estimada=models.IntegerField()
        producto_estimado=models.IntegerField()
        area_sembrada=models.IntegerField()
        area_cosechada=models.IntegerField()
	producto_obtenido=models.IntegerField()

