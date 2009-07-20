from django import forms
from django.forms import ModelForm
from precios.models import Producto
from precios.models import Mercado
from lluvia.models import EstacionDeLluvia
from semilla.models import Producto as SemillaProducto,Variedad as SemillaVariedad, CATEGORIA_CHOICES as SemillaCategoriaChoices
from lugar.models import Departamento, Municipio
from cosecha.models import Producto as CosechaProducto #esto es lo nuevo crocha

date_inputformats=['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d']

FRECUENCIA_CHOICES=(('diario','todos los datos'),('mensual','promedio mensual'),('anual','promedio anual'))
COSECHA_CHOICES=(('area estimada', 'Area estimada'),('producto estimado','Producto estimado'),('area sembrada','Area sembrada'),('area cosechada', 'Area Cosechada'),('producto obtenido','Producto obtenido'),('rendimiento estimado','Rendimiento estimado'),('rendimiento obtenido','Rendimiento obtenido'),('a    rea perdida','Area perdida'))
#COSECHA_CHOICES=(('area estimada', 'Area estimada'),('producto estimado','Producto estimado'),('area sembrada','Area sembrada'),('area cosechada', 'Area Cosechada'),('producto obtenido','Producto obtenido'),('rendimiento estimado','Rendimiento estimado'),('rendimiento obtenido','Rendimiento obtenido'),('a    rea perdida','Area perdida'),('area miscalculada','Area miscalculada'),('producto miscalculado','Producto miscalculado'))
PRECIO_MEDIDA_CHOICES=(('nativa','Unidades nativas del mercado'),('mayor','Unidades convertidas a las del mayoreo'),('menor','Unidades convertidas a las del detallista'))


class DbForm(forms.Form):
	Frecuencia=forms.MultipleChoiceField(choices=FRECUENCIA_CHOICES,required=True,initial=['diario'])
	LugarDepartamento=forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	LugarMunicipio=forms.ModelMultipleChoiceField(queryset=Municipio.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	Desde=forms.DateField(input_formats=date_inputformats)
	Hasta=forms.DateField(input_formats=date_inputformats)
	PreciosMercado=forms.ModelMultipleChoiceField(queryset=Mercado.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	PreciosProducto=forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), required=False,widget=forms.SelectMultiple(attrs={'size':'5'}))
	PreciosMedida=forms.ChoiceField(choices=PRECIO_MEDIDA_CHOICES,required=True,initial='nativo')
	CosechaVariable=forms.MultipleChoiceField(choices=COSECHA_CHOICES,required=False)
	LluviaEstacionDeLluvia=forms.ModelMultipleChoiceField(queryset=EstacionDeLluvia.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	CosechaProducto=forms.ModelMultipleChoiceField(queryset=CosechaProducto.objects.all(), required=False) #Esto es lo nuevo crocha
	IncluirLluvia=forms.BooleanField(required=False)
	SemillaProducto=forms.ModelMultipleChoiceField(queryset=SemillaProducto.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	SemillaVariedad=forms.ModelMultipleChoiceField(queryset=SemillaVariedad.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	SemillaCategoria=forms.MultipleChoiceField(choices=SemillaCategoriaChoices,required=False)

