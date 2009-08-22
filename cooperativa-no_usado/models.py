# -*- encoding: utf-8 -*-

from django.db import models
from lugar.models import Departamento, Municipio
import datetime


class Ecp(models.Model):
	nombre = models.CharField("Nombre",max_length=200, unique=True)

	def __unicode__(self):
		return self.nombre

class Cooperativa(models.Model):
	ecp = models.ForeignKey(Ecp)
	nombre_completo = models.TextField("Nombre Completo",blank=True,null=True)
	nombre_resumido = models.CharField("Nombre Resumido",max_length=200, unique=True,blank=True,null=True)
	msnm = models.IntegerField("Metros sobre el nivel del mar",max_length=10,blank=True,null=True)
	municipio = models.ForeignKey(Municipio)
	fecha_constitucion= models.DateField("Fecha de Constitucion",blank=True,null=True)
	representante_legal = models.CharField("Representante",max_length=200,blank=True,null=True)
	tecnico = models.CharField("Tecnico a cargo",max_length=200,blank=True,null=True)
	
	def __unicode__(self):
		return self.nombre_resumido
	
	class Meta:
		verbose_name_plural = "Cooperativas"

ANOS_CHOICES=[]
for i in range (datetime.date.today().year,1989,-1):
	ANOS_CHOICES.append((i,str(i)))

class Detallecoop(models.Model):
	cooperativa = models.ForeignKey(Cooperativa)
	ano = models.PositiveIntegerField(choices=ANOS_CHOICES, verbose_name="Año")
	mem_hombre = models.IntegerField("Membrecias Hombre",max_length=10, blank=True,null=True)
	mem_mujer = models.IntegerField("Membrecias Mujer",max_length=10, blank=True,null=True)
	mem_total = models.IntegerField("Membrecia Total",max_length=10, editable=False, blank=True,null=True) # este campo es calculado
	ben_hombre = models.IntegerField("Beneficiarios Hombre",max_length=10, blank=True,null=True)
	ben_mujer = models.IntegerField("Beneficiarios Mujer",max_length=10, blank=True,null=True)
	ben_total = models.IntegerField("Beneficiario Total",max_length=10, editable=False, blank=True,null=True) # este campo es calculado
	mujer_cargo = models.IntegerField("Mujeres en cargo de direccion",max_length=10, blank=True,null=True)
	
	class Meta:
		verbose_name_plural = "Detalle de cooperativa"

	def save(self, force_insert=False, force_update=False):
		self.mem_total = self.mem_hombre + self.mem_mujer
		self.ben_total = self.ben_hombre + self.ben_mujer
		super(Detallecoop,self).save(force_insert, force_update)

#comienzan modelos de comercializacion 

class Producto(models.Model):
	nombre = models.CharField("Nombre",max_length=200, unique=True)

	def __unicode__(self):
		return self.nombre

CICLO_CHOICES=[]
d=0
for i in range (datetime.date.today().year,1989,-1):
	d=i-1
	CICLO_CHOICES.append((i,str(d)+"-"+str(i)))

CERTIFICACION_CHOICES = (
    (1, 'En Proceso'),(2, 'No Certificado'),(3, 'Comercio Justo'),(4, 'Organico Biolatina'),(5, 'Organico OCIA'),(6, 'Cafe Practices'),(7, 'Especial')
)

VARIEDAD_CHOICES = (
    (1, 'Caturra'),(2, 'Catimore'),(3, 'Maracaturra'),(4, 'Borbon'),(5, 'Catuai'),(6, 'Maragojipe'),(7, 'Pacamara')
)

class Comercializacion(models.Model):
	ciclo = models.IntegerField("Ciclo de Cosecha",choices=CICLO_CHOICES,max_length=10)
	cooperativa = models.ForeignKey(Cooperativa)
	producto = models.ForeignKey(Producto)
	productor = models.IntegerField("Numero de Productores",max_length=10, blank=True)
	area = models.DecimalField("Area",max_digits=10,decimal_places=2, blank=True, help_text="Manzanas (mz)")
	produccion = models.DecimalField("Produccion",max_digits=10,decimal_places=2, blank=True, help_text="Quintales (qq)")
	rendimiento = models.DecimalField("Rendimiento",editable=False,max_digits=10,decimal_places=2, blank=True, help_text="Quintasles(qq) / Manzanas (mz)") # este campo es calculado
	exportacion = models.DecimalField("Exportacion",max_digits=10,decimal_places=2, blank=True, help_text="Quintales (qq)")
	precio_expt = models.DecimalField("Precio de venta exportacion",max_digits=10,decimal_places=2, blank=True,help_text="Dolares ($)")
	precio_merc_local = models.DecimalField("Precio de venta mercado local",max_digits=10,decimal_places=2, blank=True,help_text="Dolares ($)")
	certificacion = models.IntegerField("Tipo de certificacion",choices=CERTIFICACION_CHOICES, blank=True)
	variedad = models.IntegerField("Variedad",choices=VARIEDAD_CHOICES, blank=True)

	def save(self, force_insert=False, force_update=False):
		self.rendimiento = self.produccion / self.area
		super(Comercializacion,self).save(force_insert, force_update)
