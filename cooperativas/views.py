# -*- encoding: utf-8 -*-
from django.http import Http404
from coffin.shortcuts import render_to_response
from django.template import RequestContext
from cooperativas.models import *
from lugar.models import *
from forms import *


def render_to_html(request,template,variables):
        variables['request']=request
        new_variables=variables
        return render_to_response(template, new_variables,context_instance=RequestContext(request))

def index(request):
	s = Cooperativa.objects.all()
	return render_to_html(request,"/cooperativas/listado.html", { 's':s })

def cooperativar(request, listar_id):
	lista = Cooperativa.objects.get(pk=listar_id)
	return render_to_html(request,"/cooperativas/cooperativa_detail.html", {'lista':lista})

def detallelistar(request, deta_id):
	p = Detallecoop.objects.filter(cooperativa=deta_id)
	return render_to_html(request,"/cooperativas/cooperativa_list.html", {'p': p})

# vistas para comercializacion
def comercio(request):
	A = FormComer(request.GET)
	query_a = request.GET.get('cooperativas','')
	query_b = request.GET.get('anos', '')
	query_c = request.GET.get('productos', '')
	if query_a and query_b and query_c:
		k = Comercializacion.objects.filter(cooperativa=query_a).filter(ciclo=query_b).filter(producto=query_c)
		return render_to_response("comercializacion/comercio.html", {'A':A, 'k':k})
	else:
		l = Comercializacion.objects.all()
		return render_to_response("comercializacion/comercio.html", locals())
	
def comerciobruto(request):
	T = FormBruto(request.GET)
	query_d = request.GET.get('productos', '')
	query_f = request.GET.get('municipios','')
	query_g = request.GET.get('ciclos','')
	if query_d and query_f and query_g:
		h = Comercializacion.objects.filter(producto=query_d).filter(cooperativa__municipio=query_f).filter(ciclo=query_g)
		return render_to_response("comercializacion/comercio-bruto.html", {'T':T, 'h':h})
	else:
		i = Comercializacion.objects.all()
		return render_to_response("comercializacion/comercio-bruto.html", locals())
	
# vistas de cooperativas vienen desde lugar
def comeindex(request):
	F = FormLugar(request.GET)
	query = request.GET.get('departamentos', '')
	if query:
		j = Municipio.objects.filter(departamento=query)
		return render_to_response("cooperativa/lista-cooperativa.html", {'j':j})
	else:
		k = Departamento.objects.all()
		return render_to_response("cooperativa/lista-cooperativa.html", locals())
	
def coopmun(request, mun_id):
	a = Cooperativa.objects.filter(municipio__numero=mun_id)
	return render_to_response("cooperativa/municipio.html", {'a': a})

def verdetalle(request, deta_id):
	c = Cooperativa.objects.filter(id=deta_id)
	return render_to_response("cooperativa/detalle.html", {'c':c})

def detacompleto(request, p_id):
	b = Detallecoop.objects.filter(cooperativa=p_id)
	return render_to_response("cooperativa/completo.html", {'b':b})
