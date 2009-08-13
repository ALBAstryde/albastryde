# -*- encoding: utf-8 -*-
from proyecto.forms import *
from django.template import RequestContext
from proyectos.proyecto.models import *
from django.shortcuts import render_to_response

import os

# Consulta para saber los beneficiarios con sus detalles
def ConsulForm(request):
	query = request.GET.get('c', '')
	if query:
		results = Beneficiario.objects.filter(persona=query)
		return render_to_response("resultado.html", {'results': results})
	else:
		bene= Persona.objects.all()
		return render_to_response("resultado.html", locals())

# Consulta para saber los detalles de las personas con sus detalles y proyectos a los que pertenece
def Benefi(request):
	F = BeneficiarioForm(request.GET)
	query = request.GET.get('beneficiarios', '')
	if query:
		b = Persona.objects.filter(id=query)
		c = Beneficiario.objects.filter(persona__id=query)
		return render_to_response("persona.html", {'b': b, 'c': c})
	else:
		i = Persona.objects.all()
		return render_to_response("persona.html", locals())

# Consulta sobre los datos de los proyectos
def ConsulProyecto(request):
	P = ProyectoForm(request.GET)
	query = request.GET.get('proyectos', '')
	if query:
		j = Proyecto.objects.filter(id=query)
		ma = Beneficiario.objects.filter(proyecto__id=query)
		contar = ma.count()
		contmujer = Beneficiario.objects.filter(proyecto__id=query).filter(persona__sexo=0)
		mujer = contmujer.count()
		conthombre = Beneficiario.objects.filter(proyecto__id=query).filter(persona__sexo=1)
		hombre = conthombre.count()
		return render_to_response("proyecto.html", {'j': j, 'contar': contar, 'mujer': mujer, 'hombre': hombre, 'ma': ma})
	else:
		k = Proyecto.objects.all()
		return render_to_response("proyecto.html", locals())

#Esto es solo prueba para saber si estaban bien los datos, todos los datos los tenemos en formato CSV 

