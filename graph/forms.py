from django import forms
from django.forms import ModelForm
from precios.models import Producto
from precios.models import Mercado
from lluvia.models import EstacionDeLluvia

date_inputformats=['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d']

FRECUENCIA_CHOICES=(('diario','todos los datos'),('mensual','promedio mensual'),('anual','promedio anual'))

class DbForm(forms.Form):
	Producto=forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), required=False)
	Frecuencia=forms.MultipleChoiceField(choices=FRECUENCIA_CHOICES,required=True)
	Mercado=forms.ModelMultipleChoiceField(queryset=Mercado.objects.all(), required=False)
	EstacionDeLluvia=forms.ModelMultipleChoiceField(queryset=EstacionDeLluvia.objects.all(), required=False)
	StartDate=forms.DateField(input_formats=date_inputformats)
	EndDate=forms.DateField(input_formats=date_inputformats)
