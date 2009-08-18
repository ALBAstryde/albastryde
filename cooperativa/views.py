# -*- encoding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response
from cooperativa.models import *
from lugar.models import *
from forms import *

def index(request):
	s = Cooperativa.objects.all()
	return render_to_response("base.html", { 's':s })

def cooperativar(request, listar_id):
	lista = Cooperativa.objects.get(pk=listar_id)
	return render_to_response("cooperativa/cooperativa_detail.html", {'lista':lista})

def detallelistar(request, deta_id):
	p = Detallecoop.objects.filter(cooperativa=deta_id)
	#if k = p.cooperativa == deta_id
	return render_to_response("cooperativa/cooperativa_list.html", {'p': p})

#def comeindex(request):
#	F = FormLugar(request.GET)
#	query = request.GET.get('departamentos', '')
#	if query:
#		j = Municipio.objects.filter(departamento=query)
#		return render_to_response("cooperativa/index.html", {'j':j})
#	else:
#		k = Departamento.objects.all()
#		return render_to_response("cooperativa/index.html", locals())

