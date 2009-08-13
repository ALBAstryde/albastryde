from django.forms import ModelForm
from proyectos.proyecto.models import *
from django import forms


class BeneficiarioForm(forms.Form):
	beneficiarios = forms.ModelMultipleChoiceField(queryset=Persona.objects.all(), required=False)

class beneForm(forms.ModelForm):
	persona = forms.ModelMultipleChoiceField('Beneficiario', required=False)

class ProyectoForm(forms.Form):
	proyectos = forms.ModelMultipleChoiceField(queryset=Proyecto.objects.all(), required=False)


