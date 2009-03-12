from django.db import models
from precios.inherit_model import Approvable, Timestamped
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment

class Producto(models.Model):
	nombre = models.CharField(max_length="60")

	def __unicode__(self):
		return self.nombre

class Mercado(models.Model):
	nombre = models.CharField(max_length="60")
#	municipio = models.ForeignKey(Municipio)

	def __unicode__(self):
		return self.nombre

class Prueba(Approvable):
	mercado = models.ForeignKey(Mercado)
	producto = models.ForeignKey(Producto)
	fecha = models.DateField()
	minimo = models.DecimalField(max_digits=10,decimal_places=2)
	maximo = models.DecimalField(max_digits=10,decimal_places=2)


	def __unicode__(self):
		if self.minimo==self.maximo:
			precio= str(self.minimo)+ " cordobas"
		else:
			precio= str(self.minimo)+"-"+ str(self.maximo) + " cordobas"
#		return self.producto.nombre+" ("+self.mercado.nombre+", "+str(self.fecha)+"): " + precio
		return precio


	def get_comments(self):
	        """Returns a list of comments associated with the entry."""
	        from django.contrib.contenttypes.models import ContentType
	        ctype = ContentType.objects.get(app_label__exact='precios', name__exact='prueba')
	        return Comment.objects.filter(content_type=ctype.id, object_pk=str(self.pk))
