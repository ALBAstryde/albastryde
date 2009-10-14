# -*- encoding: utf-8 -*-

from django.db import models
from lugar.models import Departamento, Municipio #aqui se hace una importacion ficticia vos tenes que usar el de albastryde
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
	ben_hombre = models.IntegerField("Beneficiarios Hombre",max_length=10, blank=True,null=True)
	ben_mujer = models.IntegerField("Beneficiarios Mujer",max_length=10, blank=True,null=True)
	mujer_cargo = models.IntegerField("Mujeres en cargo de direccion",max_length=10, blank=True,null=True)
	
	class Meta:
		verbose_name_plural = "Detalle de cooperativa"

	def mem_total(self):
		if self.mem_hombre == None and self.mem_mujer == None:
			return 0
		elif self.mem_hombre == None and self.mem_mujer != None:
			return self.mem_mujer
		elif self.mem_hombre != None and self.mem_mujer == None:
			return self.mem_hombre
		else:
			return self.mem_hombre + self.mem_mujer
#		if self.mem_hombre != None and self.mem_hombre != 0 and self.mem_mujer != None and self.mem_mujer != 0:
#			return self.mem_hombre + self.mem_mujer
#		else:
#			return 0
	
	def ben_total(self):
		if self.ben_hombre == None and self.ben_mujer == None:
			return 0
		elif self.ben_hombre == None and self.ben_mujer != None:
			return self.ben_mujer
		elif self.ben_hombre != None and self.ben_mujer == None:
			return self.ben_hombre
		else:
			return self.ben_hombre + self.ben_mujer
#		if self.ben_hombre != None and self.ben_hombre != 0 and self.ben_mujer != None and self.ben_mujer != 0:
#			return self.ben_hombre + self.ben_mujer
#		else:
#			return 0

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
	productor = models.IntegerField("Numero de Productores",max_length=10, blank=True, null=True)
	area = models.DecimalField("Area",max_digits=10,decimal_places=2, blank=True, null=True, help_text="Manzanas (mz)")
	produccion = models.DecimalField("Produccion",max_digits=10,decimal_places=2, blank=True, null=True, help_text="Quintales (qq)")
	exportacion = models.DecimalField("Exportacion",max_digits=10,decimal_places=2, blank=True, null=True, help_text="Quintales (qq)")
	precio_expt = models.DecimalField("Precio de venta exportacion",max_digits=10,decimal_places=2, blank=True, null=True, help_text="Dolares ($)")
	precio_merc_local = models.DecimalField("Precio de venta mercado local",max_digits=10,decimal_places=2, blank=True, null=True, help_text="Dolares ($)")
	certificacion = models.IntegerField("Tipo de certificacion",choices=CERTIFICACION_CHOICES, blank=True, null=True)
	variedad = models.IntegerField("Variedad",choices=VARIEDAD_CHOICES, blank=True, null=True)

	def rendimiento(self):
		if self.produccion != None and self.produccion != 0 and self.area != None and self.area != 0:
			return "%.2f" % (self.produccion / self.area)
		else:
			return 0
