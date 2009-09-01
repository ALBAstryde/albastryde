from django.forms import ModelForm
from proyectos.models import *
from django import forms


class BeneficiarioForm(forms.Form):
	beneficiarios = forms.ModelChoiceField(queryset=Persona.objects.all(), required=False)

class ProyectoForm(forms.Form):
	proyectos = forms.ModelChoiceField(queryset=Proyecto.objects.all(), required=False)


