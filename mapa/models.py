# -*- coding: utf-8 -*-
#from django.db import models
from lugar.models import Departamento, Municipio
from climate.models import Temperatura, Precipitation, Canicula, TierraPerfil, Topografia, Erosion
# Create your models here.
# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class zones(models.Model):
    fid_agroni = models.IntegerField()
    leye = models.CharField(max_length=20)
    temp = models.CharField(max_length=1)
    temperatura=models.ForeignKey(Temperatura, related_name='temp_field',blank=True,null=True)
    prec = models.CharField(max_length=1)
    precipitation=models.ForeignKey(Precipitation, related_name='prec_field',blank=True,null=True)
    cani = models.CharField(max_length=1)
    canicula=models.ForeignKey(Canicula, related_name='cani_field',blank=True,null=True)
    perf = models.CharField(max_length=1)
    tierraperfil=models.ForeignKey(TierraPerfil, related_name='perf_field',blank=True,null=True)
    pend = models.CharField(max_length=1)
    topografia=models.ForeignKey(Topografia, related_name='pend_field',blank=True,null=True)
    eros = models.CharField(max_length=1)
    erosion=models.ForeignKey(Erosion, related_name='eros_field',blank=True,null=True)
    limi = models.CharField(max_length=4)
    fid_limite = models.IntegerField()
    departamento = models.ForeignKey(Departamento, related_name='related_dep_maps')
    municipio = models.ForeignKey(Municipio, related_name='related_mun_maps')
    fid_bosque = models.IntegerField()
    gridcode = models.IntegerField()
    count = models.FloatField()
    sum_id = models.FloatField()
    clase = models.CharField(max_length=5)
    reclasi = models.CharField(max_length=35)
    ganlech = models.CharField(max_length=7)
    gancar = models.CharField(max_length=6)
    cacao = models.CharField(max_length=5)
    clima = models.CharField(max_length=16)
    cafe = models.CharField(max_length=4)
    pltn_rie = models.CharField(max_length=8)
    teca = models.CharField(max_length=4)
    teca1 = models.CharField(max_length=5)
    okra = models.CharField(max_length=4)
    mani = models.CharField(max_length=4)
    pafric = models.CharField(max_length=6)
    mani1 = models.CharField(max_length=5)
    higuera = models.CharField(max_length=8)
    chilepic = models.CharField(max_length=8)
    tempate = models.CharField(max_length=6)
    yuca = models.CharField(max_length=4)
    cafe = models.CharField(max_length=4)
    bnan_sec = models.CharField(max_length=8)
    banan_rie = models.CharField(max_length=8)
    papa = models.CharField(max_length=4)
    gancar1 = models.CharField(max_length=7)
    maiz = models.CharField(max_length=4)
    algodon = models.CharField(max_length=7)
    ganlech1 = models.CharField(max_length=8)
    maiz_o = models.CharField(max_length=6)
    maiz_b = models.CharField(max_length=6)
    maiz_r = models.CharField(max_length=6)
    novillest = models.CharField(max_length=5)
    area = models.FloatField()
    perimeter = models.FloatField()
    hectares = models.FloatField()
    geom = models.MultiPolygonField(srid=26716)
    objects = models.GeoManager()


# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class zoninac_50000(models.Model):
    fid_agroni = models.IntegerField()
    leye = models.CharField(max_length=20)
    temp = models.CharField(max_length=1)
    prec = models.CharField(max_length=1)
    cani = models.CharField(max_length=1)
    perf = models.CharField(max_length=1)
    pend = models.CharField(max_length=1)
    eros = models.CharField(max_length=1)
    limi = models.CharField(max_length=4)
    fid_limite = models.IntegerField()
    munic_id = models.IntegerField()
    depto_id = models.IntegerField()
    depto = models.CharField(max_length=35)
    municipio = models.CharField(max_length=35)
    fid_bosque = models.IntegerField()
    gridcode = models.IntegerField()
    count = models.FloatField()
    sum_id = models.FloatField()
    clase = models.CharField(max_length=5)
    reclasi = models.CharField(max_length=35)
    ganlech = models.CharField(max_length=7)
    gancar = models.CharField(max_length=6)
    cacao = models.CharField(max_length=5)
    clima = models.CharField(max_length=16)
    cafe = models.CharField(max_length=4)
    pltn_rie = models.CharField(max_length=8)
    teca = models.CharField(max_length=4)
    teca1 = models.CharField(max_length=5)
    okra = models.CharField(max_length=4)
    mani = models.CharField(max_length=4)
    pafric = models.CharField(max_length=6)
    mani1 = models.CharField(max_length=5)
    higuera = models.CharField(max_length=8)
    chilepic = models.CharField(max_length=8)
    tempate = models.CharField(max_length=6)
    yuca = models.CharField(max_length=4)
    cafe = models.CharField(max_length=4)
    bnan_sec = models.CharField(max_length=8)
    banan_rie = models.CharField(max_length=8)
    papa = models.CharField(max_length=4)
    gancar1 = models.CharField(max_length=7)
    maiz = models.CharField(max_length=4)
    algodon = models.CharField(max_length=7)
    ganlech1 = models.CharField(max_length=8)
    maiz_o = models.CharField(max_length=6)
    maiz_b = models.CharField(max_length=6)
    maiz_r = models.CharField(max_length=6)
    novillest = models.CharField(max_length=5)
    area = models.FloatField()
    perimeter = models.FloatField()
    hectares = models.FloatField()
    geom = models.MultiPolygonField(srid=26716)
    objects = models.GeoManager()

# Auto-generated `LayerMapping` dictionary for zoninac_50000 model
zoninac_50000_mapping = {
    'fid_agroni' : 'FID_AGRONI',
    'leye' : 'LEYE',
    'temp' : 'TEMP',
    'prec' : 'PREC',
    'cani' : 'CANI',
    'perf' : 'PERF',
    'pend' : 'PEND',
    'eros' : 'EROS',
    'limi' : 'LIMI',
    'fid_limite' : 'FID_LIMITE',
    'munic_id' : 'MUNIC_ID',
    'depto_id' : 'DEPTO_ID',
    'depto' : 'DEPTO',
    'municipio' : 'MUNICIPIO',
    'fid_bosque' : 'FID_BOSQUE',
    'gridcode' : 'GRIDCODE',
    'count' : 'COUNT',
    'sum_id' : 'SUM_ID',
    'clase' : 'CLASE',
    'reclasi' : 'RECLASI',
    'ganlech' : 'GANLECH',
    'gancar' : 'GANCAR',
    'cacao' : 'CACAO',
    'clima' : 'CLIMA',
    'cafe' : 'CAFE',
    'pltn_rie' : 'PLTN_RIE',
    'teca' : 'TECA',
    'teca1' : 'TECA1',
    'okra' : 'OKRA',
    'mani' : 'MANI',
    'pafric' : 'PAFRIC',
    'mani1' : 'MANI1',
    'higuera' : 'HIGUERA',
    'chilepic' : 'CHILEPIC',
    'tempate' : 'TEMPATE',
    'yuca' : 'YUCA',
    'cafe' : 'CAÒA',
    'bnan_sec' : 'BNAN_SEC',
    'banan_rie' : 'BANAN_RIE',
    'papa' : 'PAPA',
    'gancar1' : 'GANCAR1',
    'maiz' : 'MAIZ',
    'algodon' : 'ALGODON',
    'ganlech1' : 'GANLECH1',
    'maiz_o' : 'MAIZ_O',
    'maiz_b' : 'MAIZ_B',
    'maiz_r' : 'MAIZ_R',
    'novillest' : 'NOVILLEST',
    'area' : 'AREA',
    'perimeter' : 'PERIMETER',
    'hectares' : 'HECTARES',
    'geom' : 'MULTIPOLYGON',
}
