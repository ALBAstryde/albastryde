# -*- encoding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response
from cooperativa.models import *
from lugar.models import *
from forms import *

def index(request):
	s = Cooperativa.objects.all()
	return render_to_response("/cooperativa/listado.html", { 's':s })

def cooperativar(request, listar_id):
	lista = Cooperativa.objects.get(pk=listar_id)
	return render_to_response("cooperativa/cooperativa_detail.html", {'lista':lista})

def detallelistar(request, deta_id):
	p = Detallecoop.objects.filter(cooperativa=deta_id)
	return render_to_response("cooperativa/cooperativa_list.html", {'p': p})

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
	#query_e = request.GET.get('departamentos','')
	query_f = request.GET.get('municipios','')
	query_g = request.GET.get('ciclos','')
	if query_d and query_f and query_g:
		h = Comercializacion.objects.filter(producto=query_d).filter(cooperativa__municipio=query_f).filter(ciclo=query_g)
		return render_to_response("comercializacion/comercio-bruto.html", {'T':T, 'h':h})
	else:
		i = Comercializacion.objects.all()
		return render_to_response("comercializacion/comercio-bruto.html", locals())
