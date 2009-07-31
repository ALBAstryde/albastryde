# -*- encoding: utf-8 -*-

from django.db import models
import datetime


# Create your models here.
SEXO_CHOICE=(('F', 'Femenino'),('M','Masculino'))

class Persona(models.Model):
	nombre = models.CharField(max_length=200, verbose_name="Nombre y apellido", help_text="Introduzca por favor el nombre y apellido del beneficiario")
	num_cedula = models.CharField(max_length=200, verbose_name="No. de Cedula", help_text="Introduzca por favor el número de cedula del beneficiario", null=True, blank=True)
	sexo = models.CharField(max_length=1, choices=SEXO_CHOICE, verbose_name="Sexo", help_text="Introduzca el sexo del beneficiario")
	#cooperativas = models.ManyToManyField(Cooperativa)
	
	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ['nombre']
		
class Cooperativa(models.Model):
	nombre = models.CharField(max_length=200, verbose_name="Nombre de cooperativa", help_text="Introduzca el nombre de la cooperativa")
	personas = models.ManyToManyField(Persona)
	
	def __unicode__(self):
		return self.nombre
	
	
class Producto(models.Model): # aqui usar los productos ya existente del albastryde
	nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto", help_text="Introduzca por favor el nombre del producto")
	
	def __unicode__(self):
		return self.nombre
class Variedad(models.Model):
	nombre = models.CharField(max_length=200, verbose_name="Nombre de la Variedad", help_text="Introduzca por favor el nombre de la variedad")
	producto = models.ForeignKey(Producto)
	
	def __unicode__(self):
		return self.nombre
	
class Departamento(models.Model): # aqui usar los departamentos ya existente del albastryde
	nombre = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.nombre
	
class Proyecto(models.Model):
	nombre_proy = models.CharField(max_length=200, verbose_name="Nombre del proyecto", help_text="Introduzca por favor el nombre del proyecto")
	dpto = models.ForeignKey(Departamento) # aqui usar los departamentos ya existente del albastryde
	f_inicio = models.DateField()
	f_final = models.DateField()
	producto = models.ForeignKey(Producto)
	
	def __unicode__(self):
		return self.nombre_proy
	

	
MANE_CHOICE=((1,'Organico'),(2,'Convencional'),(3,'Transición'),(4,'Semintecnificado'),(5,'Practice'),(6,'Tradicional'))

CER_CHOICE=((1,'Faire Trade'),(2,'En Proceso'),(3,'No certificado'),(4,'Comercio justo'),(5,'Organico y Faire Trade'),(6,'Biolatina'),(7,'Cafe practice'))
class Beneficiario(models.Model):
	proyectos = models.ForeignKey(Proyecto)
	personas = models.ForeignKey(Persona)
	tamano_f = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Tamaño de la Finca", help_text="Introduzca el tamaño de la finca")
	altura_pro = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Altura promedio")
	area_pro = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Area de produccion")
	area_desa = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Area en desarrollo")
	rend_pro_qq = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Rendimiento promedio en QQ")
	rend_pro_oro = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Rendimiento promedio en ORO")
	manejo = models.IntegerField(choices=MANE_CHOICE, verbose_name="Manejo")
	variedad = models.ManyToManyField(Variedad)
	certifica = models.IntegerField(choices=CER_CHOICE, verbose_name="Certificación")
	
	class Meta:
		unique_together = ['proyectos', 'personas']
	
