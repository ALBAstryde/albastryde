# -*- coding: utf-8 -*-

import datetime
import markdown
from django.db import models
import djangosearch
from django.conf import settings
from wiki.albamarkup import albamarkup
import unicodedata
from django import forms  


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

	def markdown_to_html( self ):
		markdownText= self.contenido
		images = self.imagenes.all()
    		image_ref_list = []
    		for image in images:
        		image_url = image.imagen.url
        		image_md = u"!["+image.nombre+"]("+str(image_url)+")" 
        		image_ref = u"!["+image.nombre +"]"
        		markdownText=markdownText.replace(image_ref,image_md)
    		albatranslator=albamarkup(markdownText)
    		markdownText = albatranslator.returntext
    		html = markdown.markdown( markdownText )
		self.json_data = albatranslator.json_data
		self.body_html = html
    		return True


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

