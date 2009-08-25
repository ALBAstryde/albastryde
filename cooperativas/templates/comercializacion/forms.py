from django.forms import ModelForm
from django import forms
from albastryde.lugar.models import Departamento

class FormLugar(forms.Form):
	departamentos = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
