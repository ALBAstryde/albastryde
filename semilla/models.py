# -*- encoding: utf-8 -*-

from django.db import models
from graph.models import StatisticsFormVariable
import datetime
from lugar.models import Departamento

class Producto(StatisticsFormVariable):
        pass

class Variedad(models.Model):
        nombre = models.CharField(max_length="60")
	producto=models.ForeignKey(Producto)

        def save(self):
                self.nombre=self.nombre.translate({91: None, 61: None, 38: None, 93: None}).strip() # delete u'[]=&' from string and whitespace from ends
                super(StatisticsFormVariable, self).save()

        def __unicode__(self):
                return self.producto.nombre +' ('+self.nombre+')'

        class Meta:
                ordering = ['producto','nombre']
		unique_together=['nombre','producto']


class Productor(models.Model):
        nombre = models.CharField(max_length="60")
	departamento=models.ForeignKey(Departamento)

        def save(self):
                self.nombre=self.nombre.translate({91: None, 61: None, 38: None, 93: None}).strip() # delete u'[]=&' from string and whitespace from ends
                super(StatisticsFormVariable, self).save()

        def __unicode__(self):
                return self.nombre +' ('+self.departamento+')'

        class Meta:
                ordering = ['nombre']
		unique_together=['nombre','departamento']



CATEGORIA_CHOICES=[
(1,'certificada'),
(2,'registrada'),
(3,'basica'),
(4,'genetica'),
]

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
class Semilla(models.Model):
        ano=models.PositiveIntegerField(choices=ANOS_CHOICES,verbose_name='año')
	mes=models.IntegerField(choices=MES_CHOICES)
	variedad=models.ForeignKey(Variedad)
	productor=models.ForeignKey(Productor)
	categoria=models.IntegerField(choices=CATEGORIA_CHOICES)
	cantidad=models.DecimalField(max_digits=9,decimal_places=2)
