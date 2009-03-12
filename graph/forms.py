from django import forms
from django.forms import ModelForm
from precios.models import Producto
from precios.models import Mercado

date_inputformats=['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d']
class DbForm(forms.Form):
	producto=forms.ModelMultipleChoiceField(queryset=Producto.objects.all())
	mercado=forms.ModelMultipleChoiceField(queryset=Mercado.objects.all())
	start_date=forms.DateField(input_formats=date_inputformats)
	end_date=forms.DateField(input_formats=date_inputformats)
