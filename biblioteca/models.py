# -*- encoding: utf-8 -*-

import mimetypes
import djangosearch
from django.db import models
from django.conf import settings
from djutils.features.fuzzydate import FuzzyDateField



def pdf_text_extractor(path):
	import pyPdf
	content = ""
	# Load PDF into pyPDF
	pdf = pyPdf.PdfFileReader(file(path, "rb"))
	# Iterate pages
	for i in range(0, pdf.getNumPages()):
        	# Extract text from page and add to content
        	content += pdf.getPage(i).extractText() + "\n"
	# Collapse whitespace
	content = " ".join(content.replace(u"\xa0", " ").strip().split())
	return content

          
class Autor(models.Model):
	nombre = models.CharField(max_length=200, help_text="Por favor ingrese el nombre del autor", verbose_name="Nombre")

	def __unicode__(self):
		return self.nombre
	
class Editorial(models.Model):
	nombre = models.CharField(max_length=200, help_text="Por favor ingrese el nombre de la Organización o Editorial", verbose_name="Nombre")
	
	def __unicode__(self):
		return self.nombre

class PalabraClave(models.Model):
	palabra = models.CharField(unique=True,max_length=50)

	def __unicode__(self):
		return self.palabra


class Documento(models.Model):
	nombre = models.CharField(max_length=200, help_text="Por favor ingrese le titulo del documento", verbose_name="Titulos")
	text_contents = models.TextField(blank=True,editable=False)
	autor = models.ForeignKey(Autor, verbose_name="Autor")
	fecha_publicado = FuzzyDateField(verbose_name="Fecha de publicacion")
	fecha_anadido = models.DateTimeField(editable=False, auto_now_add=True, verbose_name="Fecha añadido")
	descripcion = models.TextField(max_length=200, verbose_name="Descripcion")
	organizacion = models.ForeignKey(Editorial, verbose_name="Organizacion")
	enlace = models.URLField(verbose_name="Enlace o Link", null=True, blank=True)
        index = djangosearch.ModelIndex(text=['nombre','descripcion','text_contents'])
	palabras_claves = models.ManyToManyField(PalabraClave)
	attachment = models.FileField(upload_to="upload/documentos", verbose_name="Archivo adjunto", help_text="ADVERTENCIA: solo añadir un archivo *.pdf", null=True, blank=True)

	def get_absolute_url(self):
		return '%s%s/%s' % (settings.MEDIA_URL, settings.ATTACHMENT_FOLDER, self.id)

	def get_download_url(self):
		return '%s%s' % (settings.MEDIA_URL, self.attachment)

	def __unicode__(self):
		return self.nombre
	
        def save(self):
		if self.attachment:
			attachment_type=mimetypes.guess_type(self.attachment.path)[0]
			if attachment_type=='application/pdf':
		                super(Documento, self).save()
				self.text_contents=pdf_text_extractor(self.attachment.path).encode("ascii", "ignore")
                super(Documento, self).save()

