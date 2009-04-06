from django import forms
from django.forms import ModelForm
from precios.models import Producto
from precios.models import Mercado
from lluvia.models import EstacionDeLluvia

date_inputformats=['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d']
class DbForm(forms.Form):
	Producto=forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), required=False)
	Mercado=forms.ModelMultipleChoiceField(queryset=Mercado.objects.all(), required=False)
	EstacionDeLluvia=forms.ModelMultipleChoiceField(queryset=EstacionDeLluvia.objects.all(), required=False)
	StartDate=forms.DateField(input_formats=date_inputformats)
	EndDate=forms.DateField(input_formats=date_inputformats)
