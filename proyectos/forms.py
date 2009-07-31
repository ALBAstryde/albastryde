from django.forms import ModelForm
from proyectos.proyecto.models import *
from django import forms

class BeneficiarioForm(forms.Form):
	beneficiarios = forms.ModelMultipleChoiceField(queryset=Persona.objects.all(), required=False)
	#class Meta:
	#	model = Beneficiario
	#	fields = ('nombre',)


