# -*- encoding: utf-8 -*-

from django.db import models
from graph.models import StatisticsFormVariable
import datetime
from lugar.models import Departamento

class Producto(StatisticsFormVariable):
        pass

class Variedad(StatisticsFormVariable):
	producto=models.ForeignKey(Producto)

class Productor(StatisticsFormVariable):
	pass

CATEGORIA_CHOICES=(
(1,'certificada'),
(2,'registrada'),
(3,'basica'),
(4,'genetica'),
)

ANOS_CHOICES=[]

for i in range (datetime.date.today().year,2002,-1):
          ANOS_CHOICES.append((i,i))


MES_CHOICES=(
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10),
(11,11),
(12,12),
)
class Cosecha(models.Model):
	departamento=models.ForeignKey(Departamento)
        ano=models.PositiveIntegerField(choices=ANOS_CHOICES,verbose_name='año')
	mes=models.IntegerField(choices=MES_CHOICES)
	variedad=models.ForeignKey(Variedad)
	productor=models.ForeignKey(Productor)
	categoria=models.IntegerField(choices=CATEGORIA_CHOICES)
	cantidad=models.DecimalField(max_digits=9,decimal_places=2)
