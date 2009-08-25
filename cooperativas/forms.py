# -*- encoding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from models import Departamento, Comercializacion, Producto, Cooperativa, Municipio
import datetime

CICLO_CHOICES=[]
d=0
for i in range (datetime.date.today().year,1989,-1):
	d=i-1
	CICLO_CHOICES.append((i,str(d)+"-"+str(i)))

class FormComer(forms.Form):
	cooperativas = forms.ModelChoiceField(queryset=Cooperativa.objects.all(), required=False)
	anos = forms.ChoiceField(choices=CICLO_CHOICES, required=False)
	productos = forms.ModelChoiceField(queryset=Producto.objects.all(), required=False)
	
class FormBruto(forms.Form):
	productos = forms.ModelChoiceField(queryset=Producto.objects.all(), required=False)
	#departamentos = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
	municipios = forms.ModelChoiceField(queryset=Municipio.objects.all(), required=False)
	ciclos = forms.ChoiceField(choices=CICLO_CHOICES, required=False)
	
# forms.py proviene de lugar.models
class FormLugar(forms.Form):
	departamentos = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
