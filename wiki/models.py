# -*- coding: utf-8 -*-


# models.py
import datetime
import markdown
from django.db import models
from albastryde import djangosearch
from django.conf import settings
from wiki import albamarkup
import unicodedata
from django import forms  
from django.forms import ValidationError
#from wiki.forms import PaginaForm
# Create your models here.

def markdown_to_html( markdownText, images ):
    image_ref_list = []
    for image in images:
        image_url = image.imagen.url
        image_md = u"!["+image.nombre+"]("+str(image_url)+")" 
        image_ref = u"!["+image.nombre +"]"
        markdownText=markdownText.replace(image_ref,image_md)
    markdownText = albamarkup.ApplyMarkup(markdownText)
    html = markdown.markdown( markdownText )
    return html

class Imagen( models.Model ):
	nombre = models.CharField( max_length=100 )
	imagen = models.ImageField( upload_to="upload" )

	def __unicode__( self ):
        	return self.nombre


class Pagina(models.Model):
	nombre = models.CharField(max_length=100,unique=True)
#	nombre_standardized = models.SlugField(max_length=100,editable=False,unique=True)
	contenido = models.TextField(blank=True)
	index = djangosearch.ModelIndex(text=['nombre','contenido'])
	imagenes = models.ManyToManyField( Imagen, blank=True )

	def __unicode__( self ):
        	return self.nombre

 	def body_html( self ):
        	return markdown_to_html( self.contenido, self.imagenes.all() )

#	def standardize_nombre(self):
#        	unspanish_nombre=unicodedata.normalize('NFKD', unicode(self.nombre.strip())).encode('ascii','ignore')
#        	link_nombre=unspanish_nombre.replace(" ","-")#
#		return link_nombre
	
#	def is_valid ( self ):
#		new_nombre_standardized=self.nombre_standardize()
#		validity_check = PaginaForm(forms.model_to_dict(self))
#        	if not validity_check.is_valid():
#            		self._errors = validity_check._errors
#		if self.nombre_standardized == None or self.nombre_standardized != new_nombre_standardized:
#			a= Pagina.objects.filter(nombre_standardize=new_nombre_standardized)
#			if len(a)>0:
#				return False
#			else:
#				return validity_check.is_valid()
#		else:
#			return validity_check.is_valid()

        def dave(self,force_insert=False,force_update=False):
#		if not self.is_valid():
#            		raise Exception("Attempting to save invalid model.")
		link_nombre=self.standardize_nombre()
		if self.nombre_standardized != None and self.nombre_standardized !=link_nombre:		
			old_nombre=self.nombre_standardized
			self.nombre_standardized=link_nombre
			try:
		                super(Pagina, self).save(force_insert=True,force_update=False)
			except:
				raise Exception(u'Invalid item selected') #FIX!!! THIS MAKES NO SENSE!
			self.nombre_standardized=old_nombre
			self.delete()
		elif self.nombre_standardized == link_nombre:
	                super(Pagina, self).save(force_insert,force_update)
		elif self.nombre_standardized == None:
			self.nombre_standardized=link_nombre
	                super(Pagina, self).save(force_insert=True,force_update=False)

