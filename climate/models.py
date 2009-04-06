# -*- coding: utf-8 -*-
#from django.db import models
from lugar.models import Departamento, Municipio
# Create your models here.
# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class Temperatura(models.Model):
    temp = models.CharField(max_length=1)
    nombre = models.CharField(max_length=30)
    grados_desde =models.DecimalField(max_digits=3,decimal_places=1)
    grados_hasta =models.DecimalField(max_digits=3,decimal_places=1)
    altitud_desde =models.IntegerField()
    altitud_hasta =models.IntegerField()
    geom = models.GeometryField(srid=26716,null=True,blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.grados_desde) + "-" + str(self.grados_hasta) +" grados celsius ("+ self.nombre +")"

    def generate_map(self):
        qs= self.temp_field.all()
        polygon=qs.unionagg()
        return polygon


    def geom_save(self, force_insert=False, force_update=False):
         if self.geom== None:
             try:
                 print "Starting geom calculation for "+self.__str__()+"!"
                 self.geom=self.generate_map()
                 super(Temperatura, self).save(force_insert,force_update)
                 print self.__str__()+" saved!"
             except:
                 print "Geom calculation unsuccesful!"


class Precipitation(models.Model):
    prec = models.CharField(max_length=1)
    mm_lluvia_desde =models.IntegerField()
    mm_lluvia_hasta =models.IntegerField()
    nombre = models.CharField(max_length=30)
    geom = models.GeometryField(srid=26716,null=True,blank=True)
    objects = models.GeoManager()

    class Meta:
        verbose_name_plural='precipitationes'

    def __unicode__(self):
	description=""
	if self.nombre != None:
		description=" ("+self.nombre+")"
        return str(self.mm_lluvia_desde) + "-" + str(self.mm_lluvia_hasta)+"mm"+description

    def generate_map(self):
        qs= self.prec_field.all()
        polygon=qs.unionagg()
        return polygon


    def geom_save(self, force_insert=False, force_update=False):
         if self.geom== None:
             try:
                 print "Starting geom calculation for "+self.__str__()+"!"
                 self.geom=self.generate_map()
                 super(Precipitation, self).save(force_insert,force_update)
                 print self.__str__()+" saved!"
             except:
                 print "Geom calculation unsuccesful!"


RIESGO_CLIMATICO_CHOICES = (
    ('A', 'No hay'),
    ('B', 'Leve'),
    ('C', 'Moderado'),
    ('D', 'Alto'),
    ('E', 'Muy Alto'),
)

#RIESGO_CLIMATICO_CHOICES =['No hay','Leve','Moderado','Alto','Muy Alto']

class Canicula(models.Model):
    cani = models.CharField(max_length=1)
    meses_lluvia_desde =models.IntegerField()
    meses_lluvia_hasta =models.IntegerField()
    canicula_duracion_desde =models.IntegerField()
    canicula_duracion_hasta =models.IntegerField()
    nombre =models.CharField(null=True,max_length=30,blank=True)
    riesgo_climatico =models.CharField(null=True,max_length=1,choices=RIESGO_CLIMATICO_CHOICES)
    geom = models.GeometryField(srid=26716,null=True,blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
	lluvia=str(self.meses_lluvia_desde)
	if self.meses_lluvia_desde != self.meses_luvia_hasta:
	    lluvia=str(self.meses_lluvia_desde)+"-"+str(self.meses_lluvia_hasta)	
	canicula=str(self.canicula_duracion_desde)
	if self.canicula_duracion_desde != self.canicula_duracion_hasta:
	    canicula=str(self.canicula_duracion_desde)+"-"+str(self.canicula_duracion_hasta)	
        return lluvia+" meses, "+canicula+" dias"

    def generate_map(self):
        qs= self.cani_field.all()
        polygon=qs.unionagg()
        return polygon


    def geom_save(self, force_insert=False, force_update=False):
         if self.geom== None:
             try:
                 print "Starting geom calculation for "+self.nombre+"!"
                 self.geom=self.generate_map()
                 super(Canicula, self).save(force_insert,force_update)
                 print self.nombre+" saved!"
             except:
                 print "Geom calculation unsuccesful!"


class Textura(models.Model):
    Simbolo =models.CharField(max_length=2)
    Nombre =models.CharField(max_length=30)

    def __unicode__(self):
	return self.Simbolo

FERTILIDAD_CHOICES = (
    ('A', 'Alta'),
    ('B', 'Media'),
    ('C', 'Baja'),
    ('D', 'Muy Baja'),
)
ESTRUCTURA_CHOICES = (
    ('A', 'Bueno'),
    ('B', 'Moderado'),
    ('C', 'Debil'),
    ('D', 'Deficiente'),
    ('E', 'No hay'),
)
DRENAJE_CHOICES = (
    ('A', 'Bueno'),
    ('B', 'Moderado'),
    ('C', 'Moderado Excesivo'),
    ('D', 'Excesivo'),
)


#FERTILIDAD_CHOICES = ['Alta','Media','Baja','Muy baja']
#ESTRUCTURA_CHOICES = ['Bueno','Moderado','Debil','Deficiente','No hay']
#DRENAJE_CHOICES = ['Bueno','Moderado Excesivo','Excesivo','Moderado']
    

class TierraPerfil(models.Model):
    perf = models.CharField(max_length=1)
    geom = models.GeometryField(srid=26716,null=True,blank=True)
    fertilidad =models.CharField(null=True,max_length=1,choices=FERTILIDAD_CHOICES)
    drenaje_interno =models.CharField(null=True,max_length=1,choices=DRENAJE_CHOICES)
    grado_de_estructura =models.CharField(max_length=1,choices=ESTRUCTURA_CHOICES)
    objects = models.GeoManager()
    textura_superficie=models.ManyToManyField(Textura,related_name='superficie')
    textura_subsuelo=models.ManyToManyField(Textura,related_name='subsuelo')

    def __unicode__(self):
	return  u'%s' % self.perf

    class Meta:
        verbose_name_plural='tierra perfiles'


    def generate_map(self):
        qs= self.perf_field.all()
        polygon=qs.unionagg()
        return polygon


    def geom_save(self, force_insert=False, force_update=False):
         if self.geom== None:
             try:
                 print "Starting geom calculation for "+self.__str__()+"!"
                 self.geom=self.generate_map()
                 super(TierraPerfil, self).save(force_insert,force_update)
                 print self.__str__()+" saved!"
             except:
                 print "Geom calculation unsuccesful!"


class Topografia(models.Model):
    pend = models.CharField(max_length=1)
    geom = models.GeometryField(srid=26716,null=True,blank=True)
    Nombre =models.CharField(max_length=30)
    percentaje_desde =models.DecimalField(max_digits=3,decimal_places=1)
    percentaje_hasta =models.DecimalField(max_digits=3,decimal_places=1)
    objects = models.GeoManager()

    def __unicode__(self):
	return str(self.percentaje_desde)+"-"+str(self.percentaje_hasta)+"%"

    def generate_map(self):
        qs= self.pend_field.all()
        polygon=qs.unionagg()
        return polygon


    def geom_save(self, force_insert=False, force_update=False):
         if self.geom== None:
             try:
                 print "Starting geom calculation for "+self.__str__()+"!"
                 self.geom=self.generate_map()
                 super(Topografia, self).save(force_insert,force_update)
                 print self.__str__()+" saved!"
             except:
                 print "Geom calculation unsuccesful!"



class Erosion(models.Model):
    eros = models.CharField(max_length=1)
    nombre =models.CharField(max_length=30)
    descripcion =models.CharField(max_length=150)
    geom = models.GeometryField(srid=26716,null=True,blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
	return self.nombre

    class Meta:
        verbose_name_plural='erosiones'


    def generate_map(self):
        qs= self.eros_field.all()
        polygon=qs.unionagg()
        return polygon


    def geom_save(self, force_insert=False, force_update=False):
         if self.geom== None:
             try:
                 print "Starting geom calculation for "+self.__str__()+"!"
                 self.geom=self.generate_map()
                 super(Erosion, self).save(force_insert,force_update)
                 print self.__str__()+" saved!"
             except:
                 print "Geom calculation unsuccesful!"
