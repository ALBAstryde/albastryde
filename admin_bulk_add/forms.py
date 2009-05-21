from django import forms
from django.forms import ModelForm
from lluvia.models import EstacionDeLluvia
from precios.models import Mercado

import datetime

date_inputformats=['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d']

ANO_CHOICES=[]

for i in range (datetime.date.today().year,1920,-1):
	ANO_CHOICES.append((i,i))

MES_CHOICES=[]

for i in range(1,12):
	MES_CHOICES.append((i,i))

DIA_CHOICES=[]

for i in range(1,31):
	DIA_CHOICES.append((i,i))


class LluviaParameterForm(forms.Form):
	estacion_de_lluvia=forms.ModelChoiceField(queryset=EstacionDeLluvia.objects.all(), required=True)
	mes=forms.ChoiceField(required=True,choices=MES_CHOICES)
	ano=forms.ChoiceField(required=True,choices=ANO_CHOICES)

class PreciosParameterForm(forms.Form):
	mercado=forms.ModelChoiceField(queryset=Mercado.objects.all(), required=True)
	dia=forms.ChoiceField(required=True,choices=DIA_CHOICES)
	mes=forms.ChoiceField(required=True,choices=MES_CHOICES)
	ano=forms.ChoiceField(required=True,choices=ANO_CHOICES)
