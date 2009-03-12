from django import forms
#from django.forms import ModelForm
from wiki.models import Pagina

class PaginaForm(forms.ModelForm):
	class Meta:
       		model = Pagina
	
#	def clean(self):
#		old_nombre_standardized = self.cleaned_data.get("nombre_standardized")
#		new_nombre_standardized = self.nombre_standardize()
#		if new_nombre_standardized != old_nombre_standardized:
#			raise forms.ValidationError("new name!")
