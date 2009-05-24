from django import forms
from django.forms import ModelForm
from precios.models import Producto
from precios.models import Mercado
from lluvia.models import EstacionDeLluvia
from lugar.models import Departamento, Municipio

date_inputformats=['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d']

FREQUENCY_CHOICES=(('daily','todos los datos'),('monthly','promedio mensual'),('annualy','promedio anual'))

class DbForm(forms.Form):
	Departamento=forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	Municipio=forms.ModelMultipleChoiceField(queryset=Municipio.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	Producto=forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	Frequency=forms.MultipleChoiceField(choices=FREQUENCY_CHOICES,required=True,initial=['diario'])
	Mercado=forms.ModelMultipleChoiceField(queryset=Mercado.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	EstacionDeLluvia=forms.ModelMultipleChoiceField(queryset=EstacionDeLluvia.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size':'5'}))
	IncluirLluvia=forms.BooleanField(required=False)
	Desde=forms.DateField(input_formats=date_inputformats)
	Hasta=forms.DateField(input_formats=date_inputformats)
