from django.db import models
from lugar.models import Departamento, Municipio


# Create your models here.
class Cosecha(models.Model):
        departamento=models.ForeignKey(Departamento)
	municipio=models.ForeignKey(Municipio)
        year=models.DateField()
        tiempo_year=models.CharField(max_length=12)
        producto_nombre=models.CharField(max_length="60")
        area_estimada=models.IntegerField()
        producto_estimado=models.IntegerField()
        rendimiento_estimado=models.IntegerField()
        area_sembrada=models.IntegerField()
        area_perdida=models.IntegerField()
        area_cosechada=models.IntegerField()
        producto_obtenido=models.IntegerField()
        rendimiento_obtenido=models.IntegerField()

