from django import forms
from django.forms import ModelForm
from precios.models import Producto
from precios.models import Mercado
from lluvia.models import EstacionDeLluvia
from lugar.models import Departamento, Municipio
from cosecha.models import Producto as CosechaProducto #esto es lo nuevo crocha

date_inputformats=['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d']

FRECUENCIA_CHOICES=(('diario','todos los datos'),('mensual','promedio mensual'),('anual','promedio anual'))
COSECHA_CHOICES=(('area estimada', 'Area estimada'),('producto estimado','Producto estimado'),('area sembrada','Area sembrada'),('area cosechada', 'Area Cosechada'),('producto obtenido','Producto obtenido'),('rendimiento estimado','Rendimiento estimado'),('rendimiento obtenido','Rendimiento obtenido'),('a    rea perdida','Area perdida'))

class DbForm(forms.Form):
	Departamento=forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	Municipio=forms.ModelMultipleChoiceField(queryset=Municipio.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	Producto=forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	Frecuencia=forms.MultipleChoiceField(choices=FRECUENCIA_CHOICES,required=True,initial=['diario'])
	CosechaVariable=forms.MultipleChoiceField(choices=COSECHA_CHOICES,required=False)
	Mercado=forms.ModelMultipleChoiceField(queryset=Mercado.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	EstacionDeLluvia=forms.ModelMultipleChoiceField(queryset=EstacionDeLluvia.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	CosechaProducto=forms.ModelMultipleChoiceField(queryset=CosechaProducto.objects.all(), required=False) #Esto es lo nuevo crocha
	IncluirLluvia=forms.BooleanField(required=False)
	Desde=forms.DateField(input_formats=date_inputformats)
	Hasta=forms.DateField(input_formats=date_inputformats)
