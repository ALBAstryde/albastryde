# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
import datetime

ANOS_CHOICES=[]

for i in range (datetime.date.today().year,1979,-1):
          ANOS_CHOICES.append((i,str(i)))
          
# Create your models here.
class Autor(models.Model):
	nombre = models.CharField(max_length=200, help_text="Por favor ingrese el nombre del autor", verbose_name="Nombre")

	def __unicode__(self):
		return self.nombre
	
class Editorial(models.Model):
	nombre = models.CharField(max_length=200, help_text="Por favor ingrese el nombre de la Organización o Editorial", verbose_name="Nombre")
	
	def __unicode__(self):
		return self.nombre

class Biblioteca(models.Model):
	#content_type = models.CharField(max_length=5, blank=True, null=True)
	name = models.CharField(max_length=200, help_text="Por favor ingrese le titulo del documento", verbose_name="Titulos")
	autor = models.ForeignKey(Autor, verbose_name="Autor")
	ano = models.PositiveIntegerField(choices=ANOS_CHOICES, verbose_name="Año de publicacion")
	fecha = models.DateTimeField(editable=False, auto_now_add=True)
	decrip = models.TextField(max_length=200, verbose_name="Descripcion")
	organizacion = models.ForeignKey(Editorial, verbose_name="Organizacion")
	palabra_clave = models.CharField(max_length=200, help_text="Por favor introduzca unas palabras claves separadas con espacio que hagan referencia al documento", verbose_name="Palabra Clave o Descriptor")
	enlace = models.URLField(verbose_name="Enlace o Link", null=True, blank=True)
	attachment = models.FileField(upload_to="attachments", verbose_name="Archivo adjunto", help_text="ADVERTENCIA: solo añadir un archivo *.pdf", null=True, blank=True)

	def get_absolute_url(self):
		return '%s%s/%s' % (settings.MEDIA_URL, settings.ATTACHMENT_FOLDER, self.id)

	def get_download_url(self):
		return '%s%s' % (settings.MEDIA_URL, self.attachment)

	def __unicode__(self):
		return self.name
	
