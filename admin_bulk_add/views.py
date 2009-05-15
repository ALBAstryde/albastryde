# -*- coding: utf-8 -*-
from admin_bulk_add.forms import LluviaParameterForm

import calendar
from django import forms
from django.forms.models import modelformset_factory
from lluvia.models import Prueba as LluviaPrueba
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from urllib import quote_plus, unquote_plus
import unicodedata
import settings
import re


def render_to_html(request,template,variables):
	variables['request']=request
	new_variables=variables
        return render_to_response(template, new_variables,context_instance=RequestContext(request))

#class LluviaPruebaForm(forms.ModelForm):
#	class Meta:
#		model=LluviaPrueba


def lluvia(request,ano=None,mes=None,estacion_de_lluvia_id=None):
	if ano == None:
		if ('EstacionDeLluvia' in request.GET) and request.GET['EstacionDeLluvia'].strip():
                	estacion_de_lluvia_id = request.GET['EstacionDeLluvia']
                	ano = request.GET['Ano']
                	mes = request.GET['Mes']
			return HttpResponseRedirect("/admin/bulkadd/lluvia/"+estacion_de_lluvia_id+"/"+ano+"/"+mes+"/")
		else:
			form=LluviaParameterForm()
			return render_to_html(request,"bulk_add_form.html", {'form':form})
	else:
		LluviaPruebaFormSet = modelformset_factory(LluviaPrueba,extra=0)
		datelist=[]
		for day in range(1,calendar.monthrange(int(ano),int(mes))[1]):
			datelist.append({'estacion':int(estacion_de_lluvia_id),'fecha':str(ano)+'-'+str(mes)+'-'+str(day)})
		formset=LluviaPruebaFormSet(initial=datelist)
		form = formset
		return render_to_html(request,"bulk_add_form_lluvia.html", {"form":form})



def precios(request,tag_name=None):
	return render_to_html(request,"bulk_add_form.html", {})

