# -*- encoding: utf-8 -*-


from albastryde.nicalocals import NICedulaNumberField
from albastryde.nicalocals import NIPhoneNumberField
from django.db.models.fields import Field
from lugar.models import Departamento
from precios.models import Producto
from django.db import models
import datetime

class PhoneNumberField(Field):
	def get_internal_type(self):
		return "PhoneNumberField"

	def db_type(self):
		return 'varchar(20)'

	def formfield(self, **kwargs):
		defaults = {'form_class': NIPhoneNumberField}
		defaults.update(kwargs)
		return super(PhoneNumberField, self).formfield(**defaults)

class CedulaNumberField(Field):
	def get_internal_type(self):
		return "CedulaNumberField"

	def db_type(self):
		return 'varchar(16)'

	def formfield(self, **kwargs):
		defaults = {'form_class': NICedulaNumberField}
		defaults.update(kwargs)
		return super(CedulaNumberField, self).formfield(**defaults)

SEXO_CHOICE=((0, 'Femenino'),(1,'Masculino'))

class Cooperativa(models.Model):
	nombre = models.CharField(max_length=200, verbose_name="Nombre de cooperativa", help_text="Introduzca el nombre de la cooperativa")
	#miembros = models.ManyToManyField(Persona)
	#jefe = models.ForeignKey(Persona,blank=True,default=None)
	direccion = models.CharField(max_length=250,blank=True,default=None)
	correo_electronico = models.EmailField(max_length=80,default=None,blank=True)
	telefono = PhoneNumberField(default=None,blank=True)

	def __unicode__(self):
		return self.nombre
	

class Persona(models.Model):
	nombre = models.CharField(max_length=200, verbose_name="Nombre y apellido", help_text="Introduzca por favor el nombre")
	numero_cedula = CedulaNumberField(verbose_name="No. de Cedula", help_text="Introduzca por favor el número de cedula", blank=True, null=True)
	sexo = models.IntegerField(max_length=1, choices=SEXO_CHOICE, verbose_name="Sexo", help_text="Introduzca el sexo del beneficiario")
	direccion = models.CharField(max_length=250,blank=True,default=None)
	correo_electronico = models.EmailField(max_length=80,default=None,blank=True)
	telefono = PhoneNumberField(default=None,blank=True)
	cooperativa = models.ManyToManyField(Cooperativa)
	
	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ['nombre']
		

	
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
	nombre = models.CharField(max_length=200, verbose_name="Nombre del proyecto", help_text="Introduzca por favor el nombre del proyecto")
	departamento = models.ForeignKey(Departamento) # aqui usar los departamentos ya existente del albastryde
	fecha_inicio = models.DateField()
	fecha_final = models.DateField()
	producto = models.ForeignKey(Producto)
	
	def __unicode__(self):
		return self.nombre
	
MANEJO_CHOICES=((1,'Organico'),(2,'Convencional'),(3,'Transición'),(4,'Semintecnificado'),(5,'Practice'),(6,'Tradicional'),(7,'Tecnificado'))

CERTIFICADA_CHOICES=((1,'En Proceso'),(2,'No certificado'),(3,'Comercio justo'),(4,'Organico'),(5,'Biolatina'),(6,'Cafe practice'))

class Beneficiario(models.Model):
	proyecto = models.ForeignKey(Proyecto)
	persona = models.ForeignKey(Persona)
	tamano_de_finca = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Tamaño de la Finca", help_text="Introduzca el tamaño de la finca")
	altura_promedio = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Altura promedio")
	area_de_produccion = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Area de produccion")
	area_en_desarollo = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Area en desarrollo")
	rendimiento_promedio_en_qq = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Rendimiento promedio en QQ")
	rendimiento_promedio_en_oro = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="Rendimiento promedio en ORO")
	manejo = models.IntegerField(choices=MANEJO_CHOICES, verbose_name="Manejo", blank=True, null=True)
	variedad = models.ManyToManyField(Variedad)
	certificada = models.IntegerField(choices=CERTIFICADA_CHOICES, verbose_name="Certificación", blank=True, null=True)
	
	class Meta:
		unique_together = ['proyecto', 'persona']
		
	def __unicode__(self):
		return '%s,Proyecto %s' % (self.persona.nombre, self.proyecto.nombre)
	
