# -*- coding: utf-8 -*-
from admin_bulk_add.forms import LluviaParameterForm, PreciosParameterForm

import calendar
from django import forms
from django.forms.models import modelformset_factory
from lluvia.models import Prueba as LluviaPrueba
from precios.models import Prueba as PreciosPrueba
from precios.models import Mercado, Producto
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

def lluvia(request,ano=None,mes=None,estacion_de_lluvia=None):
	app_label="lluvia"
	model_label="prueba"
	title="Añadir mes de lluvia"
	if ano == None:
		if ('estacion_de_lluvia' in request.GET) and request.GET['estacion_de_lluvia'].strip():
                	estacion_de_lluvia = request.GET['estacion_de_lluvia']
                	ano = request.GET['ano']
                	mes = request.GET['mes']
			return HttpResponseRedirect("/admin/lluvia/prueba/bulk_add/"+estacion_de_lluvia+"/"+ano+"/"+mes+"/")
		else:
			form=LluviaParameterForm()
			return render_to_html(request,"bulk_add_form_firstpage.html", {'form':form,'app_label':app_label,'model_label':model_label,'title':title})
	else:
		next_set_description="Grabar y añadir proximo mes"
		if request.method == "POST":
			LluviaPruebaFormSet = modelformset_factory(LluviaPrueba)
			data = request.POST.copy()
			form = LluviaPruebaFormSet(data=data)
			if form.is_valid():
				form.save()
			else:
				return render_to_html(request,"bulk_add_form.html", {"form":form,"next_set_description":next_set_description,"app_label":app_label,"model_label":model_label,"title":title})
			if data.has_key('_next_set'):
				mes=int(mes)
				ano=int(ano)
				if mes < 12:
					mes += 1
				else:
					ano += 1
					mes = 1
				mes=str(mes)
				ano=str(ano)
				return HttpResponseRedirect("/admin/lluvia/prueba/bulk_add/"+estacion_de_lluvia+"/"+ano+"/"+mes+"/")
			elif data.has_key('_continue_editing'):
				return HttpResponseRedirect("/admin/lluvia/prueba/bulk_add/"+estacion_de_lluvia+"/"+ano+"/"+mes+"/")
			else:
				return HttpResponseRedirect("/admin/lluvia/")
		else:
			queryset=LluviaPrueba.objects.filter(fecha__year=int(ano)).filter(fecha__month=int(mes)).filter(estacion=int(estacion_de_lluvia))
			if len(queryset) > 0:
				LluviaPruebaFormSet = modelformset_factory(LluviaPrueba,extra=(calendar.monthrange(int(ano),int(mes))[1]-len(queryset)))
				form = LluviaPruebaFormSet(queryset=queryset)
			else:
				initial_list=[]
				for dia in range(1,calendar.monthrange(int(ano),int(mes))[1]+1):
					if mes > 9:
						mes_str=str(mes)
					else:
						mes_str="0"+str(mes)
					if dia > 9:
						dia_str=str(dia)
					else:
						dia_str="0"+str(dia)
					initial_list.append({'estacion':str(estacion_de_lluvia),'milimetros_de_lluvia':'0.0','fecha':str(ano)+'-'+mes_str+'-'+dia_str})
				LluviaPruebaFormSet = modelformset_factory(LluviaPrueba,extra=len(initial_list))
				form = LluviaPruebaFormSet(initial=initial_list,queryset=LluviaPrueba.objects.none())
			return render_to_html(request,"bulk_add_form.html", {"form":form,"next_set_description":next_set_description,"app_label":app_label,"model_label":model_label,"title":title})

def precios(request,ano=None,mes=None,dia=None,mercado=None):
	app_label="precios"
	model_label="prueba"
	title="Añadir precios de una fecha en un mercado"
	if ano == None:
		if ('mercado' in request.GET) and request.GET['mercado'].strip():
                	mercado = request.GET['mercado']
                	ano = request.GET['ano']
                	mes = request.GET['mes']
                	dia = request.GET['dia']
			return HttpResponseRedirect("/admin/precios/prueba/bulk_add/"+mercado+"/"+ano+"/"+mes+"/"+dia+"/")
		else:
			form=PreciosParameterForm()
			return render_to_html(request,"bulk_add_form_firstpage.html", {'form':form,'app_label':app_label,'model_label':model_label,'title':title})
	else:
		next_set_description="Grabar y añadir datos del proximo mercado"
		if request.method == "POST":
			PreciosPruebaFormSet = modelformset_factory(PreciosPrueba)
			data = request.POST.copy()
			form = PreciosPruebaFormSet(data=data)
			if form.is_valid():
				form.save()
			else:
				return render_to_html(request,"bulk_add_form.html", {"form":form,"next_set_description":next_set_description,"app_label":app_label,"model_label":model_label,"title":title})
			if data.has_key('_next_set'):
				mercado=int(mercado)
				if mercado < len(Mercado.objects.all()):
					mercado = 1
				mercado=str(mercado)
				return HttpResponseRedirect("/admin/precios/prueba/bulk_add/"+mercado+"/"+ano+"/"+mes+"/"+dia+"/")
			elif data.has_key('_continue_editing'):
				return HttpResponseRedirect("/admin/precios/prueba/bulk_add/"+mercado+"/"+ano+"/"+mes+"/"+dia+"/")
			else:
				return HttpResponseRedirect("/admin/precios/")
		else:
			queryset=PreciosPrueba.objects.filter(fecha__year=int(ano)).filter(fecha__month=int(mes)).filter(fecha__day=int(dia)).filter(mercado=int(mercado))
			productos=Producto.objects.all()
			if len(queryset) > 0:
				PreciosPruebaFormSet = modelformset_factory(PreciosPrueba,extra=(len(productos)-len(queryset)))
				form = LluviaPruebaFormSet(queryset=queryset)
			else:
				initial_list=[]
				if mes > 9:
					mes_str=str(mes)
				else:
					mes_str="0"+str(mes)
				if dia > 9:
					dia_str=str(dia)
				else:
					dia_str="0"+str(dia)
				for producto in productos.iterator():
					initial_list.append({'mercado':str(mercado),'producto':str(producto.id),'fecha':str(ano)+'-'+mes_str+'-'+dia_str})
				PreciosPruebaFormSet = modelformset_factory(PreciosPrueba,extra=len(initial_list))
				form = PreciosPruebaFormSet(initial=initial_list,queryset=PreciosPrueba.objects.none())
			return render_to_html(request,"bulk_add_form.html", {"form":form,"next_set_description":next_set_description,"app_label":app_label,"model_label":model_label,"title":title})
