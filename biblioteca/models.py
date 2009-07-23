# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings
import datetime

          
class Autor(models.Model):
	nombre = models.CharField(max_length=200, help_text="Por favor ingrese el nombre del autor", verbose_name="Nombre")

	def __unicode__(self):
		return self.nombre
	
class Editorial(models.Model):
	nombre = models.CharField(max_length=200, help_text="Por favor ingrese el nombre de la Organización o Editorial", verbose_name="Nombre")
	
	def __unicode__(self):
		return self.nombre

class PalabraClave(models.Model):
	nombre = models.CharField(primary_key=True)

class Biblioteca(models.Model):
	#content_type = models.CharField(max_length=5, blank=True, null=True)
	nombre = models.CharField(max_length=200, help_text="Por favor ingrese le titulo del documento", verbose_name="Titulos")
	autor = models.ForeignKey(Autor, verbose_name="Autor")
	publicado = models.FuzzyDateField(choices=ANOS_CHOICES, verbose_name="Año de publicacion")
	fecha = models.DateTimeField(editable=False, auto_now_add=True)
	descripcion = models.TextField(max_length=200, verbose_name="Descripcion")
	organizacion = models.ForeignKey(Editorial, verbose_name="Organizacion")
	palabras_claves = models.ManyToManyField(PalabraClave)
	enlace = models.URLField(verbose_name="Enlace o Link", null=True, blank=True)
	attachment = models.FileField(upload_to="attachments", verbose_name="Archivo adjunto", help_text="ADVERTENCIA: solo añadir un archivo *.pdf", null=True, blank=True)

	def get_absolute_url(self):
		return '%s%s/%s' % (settings.MEDIA_URL, settings.ATTACHMENT_FOLDER, self.id)

	def get_download_url(self):
		return '%s%s' % (settings.MEDIA_URL, self.attachment)

	def __unicode__(self):
		return self.name
	
