# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from thumbs import ImageWithThumbsField

REGION=((1,"Region Pacifico Norte"),(2,"Region Pacifico Central"),(3,"Region Pacifico Sur"),(4,"Region Las Segovias"),(5,"Region Central Norte"),(6,"Region Central Este"),(7,"Region Caribe Norte(RAAN)"),(8,"Region Caribe Sur(RAAS)"),(9,"Region del Rio San Juan"))

class Tipo(models.Model):
	nombre = models.CharField("Tipo",max_length=200)
	
	def __unicode__(self):
		return self.nombre
	
	class Meta:
		ordering = ['nombre']
		verbose_name_plural = "Tipo de Mapa"

class Mapa(models.Model):
	ano = models.DateField("Año", help_text='Fecha del mapa')
	region = models.IntegerField("Region",choices=REGION,max_length=1)
	tipo = models.ForeignKey(Tipo)
	Descripicion = models.TextField("Descripcion adicional")
	adjunto = ImageWithThumbsField(upload_to="attachment",help_text="Subir la imagen del mapa .jpg",sizes=((120,150),(360,480)))

	class Meta:
		ordering = ['region']
		verbose_name_plural = "Mapas tematicos por region"
		
	def __unicode__(self):
		return self.region

	def imagen(self):
		return '%s/%s' % (settings.MEDIA_URL, self.adjunto)
	
	
	
