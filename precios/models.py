from django.db import models
from graph.models import Approvable,StatisticsFormVariable
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from lugar.models import Municipio

class Medida(models.Model):
	medida_mayor=models.CharField(max_length=15,blank=True)
	medida_menor=models.CharField(max_length=15,blank=True)
	factor_para_convertir=models.DecimalField(max_digits=10,decimal_places=2,blank=True)

	def __unicode__(self):
		return str(self.factor_para_convertir)+' '+medida_menor+ ' = '+medida_mayor

	
class Producto(StatisticsFormVariable):
	id = models.IntegerField(primary_key=True)
	medida = models.ForeignKey(Medida)
	se_vende_en_mayor = models.BooleanField()
	se_vende_en_menor = models.BooleanField()
	se_vende_en_supermercado = models.BooleanField()

class Mercado(StatisticsFormVariable):	
	mayor = models.BooleanField()
	id = models.IntegerField(primary_key=True)
	municipio = models.ForeignKey(Municipio,null=True)

class Prueba(Approvable):
	mercado = models.ForeignKey(Mercado)
	producto = models.ForeignKey(Producto)
	fecha = models.DateField()
	minimo = models.DecimalField(max_digits=10,decimal_places=2)
	maximo = models.DecimalField(max_digits=10,decimal_places=2)

	def minimo_mayor(self):
		if self.mercado.mayor==True:
			return self.minimo
		else:
			return self.minimo*self.producto.factor_para_convertir

	def maximo_mayor(self):
		if self.mercado.mayor==True:
			return self.maximo
		else:
			return self.maximo*self.producto.factor_para_convertir

	def minimo_menor(self):
		if self.mercado.mayor==True:
			return self.minimo/self.producto.factor_para_convertir
		else:
			return self.minimo

	def maximo_menor(self):
		if self.mercado.mayor==True:
			return self.maximo/self.producto.factor_para_convertir
		else:
			return self.maximo

	def get_medida(self):
		if self.mercado.mayor==True:
			return self.medida_mayor()
		else:
			return self.medida_menor()

	def medida_mayor(self):
		return self.producto.medida.medida_mayor

	def medida_menor(self):
		return self.producto.medida.medida_menor

	def __unicode__(self):
		if self.minimo==self.maximo:
			precio= str(self.minimo)+ " C$/"+self.get_medida()
		else:
			precio= str(self.minimo)+"-"+ str(self.maximo) + " C$"+self.get_medida()
#		return self.producto.nombre+" ("+self.mercado.nombre+", "+str(self.fecha)+"): " + precio
		return precio

	def get_comments(self):
	        """Returns a list of comments associated with the entry."""
	        from django.contrib.contenttypes.models import ContentType
	        ctype = ContentType.objects.get(app_label__exact='precios', name__exact='prueba')
	        return Comment.objects.filter(content_type=ctype.id, object_pk=str(self.pk))
