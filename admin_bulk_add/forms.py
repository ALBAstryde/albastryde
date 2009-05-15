from django import forms
from django.forms import ModelForm
from lluvia.models import EstacionDeLluvia

import datetime

date_inputformats=['%d.%m.%Y','%d/%m/%Y','%Y-%m-%d']

ANO_CHOICES=[]

for i in range (datetime.date.today().year,1920,-1):
          ANO_CHOICES.append((i,i))

MES_CHOICES=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12))


class LluviaParameterForm(forms.Form):
	estacion_de_lluvia=forms.ModelChoiceField(queryset=EstacionDeLluvia.objects.all(), required=True)
	mes=forms.ChoiceField(required=True,choices=MES_CHOICES)
	ano=forms.ChoiceField(required=True,choices=ANO_CHOICES)
