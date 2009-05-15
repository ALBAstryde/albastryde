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


def lluvia(request,ano=None,mes=None,estacion_de_lluvia=None):
	if ano == None:
		if ('estacion_de_lluvia' in request.GET) and request.GET['estacion_de_lluvia'].strip():
                	estacion_de_lluvia = request.GET['estacion_de_lluvia']
                	ano = request.GET['ano']
                	mes = request.GET['mes']
			return HttpResponseRedirect("/admin/lluvia/bulk_add/"+estacion_de_lluvia+"/"+ano+"/"+mes+"/")
		else:
			form=LluviaParameterForm()
			return render_to_html(request,"bulk_add_form.html", {'form':form})
	else:
		queryset=LluviaPrueba.objects.filter(fecha__year=int(ano)).filter(fecha__month=int(mes)).filter(estacion=int(estacion_de_lluvia))
		if len(queryset) > 0:
			LluviaPruebaFormSet = modelformset_factory(LluviaPrueba,extra=(calendar.monthrange(int(ano),int(mes))[1]-len(queryset)))
			form = LluviaPruebaFormSet(queryset=queryset)
		else:
			initial_list=[]
			for day in range(1,calendar.monthrange(int(ano),int(mes))[1]+1):
				initial_list.append({'estacion':str(estacion_de_lluvia),'fecha':str(ano)+'-'+str(mes)+'-'+str(day)})
			LluviaPruebaFormSet = modelformset_factory(LluviaPrueba,extra=len(initial_list))
			form = LluviaPruebaFormSet(initial=initial_list,queryset=LluviaPrueba.objects.none())
		return render_to_html(request,"bulk_add_form_lluvia.html", {"form":form})



def precios(request,tag_name=None):
	return render_to_html(request,"bulk_add_form.html", {})

