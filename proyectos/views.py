# -*- encoding: utf-8 -*-
from proyectos.forms import BeneficiarioForm, ProyectoForm
from django.template import RequestContext
from proyectos.models import Beneficiario, Persona, Proyecto
from coffin.shortcuts import render_to_response

import os

def render_to_html(request,template,variables):
        variables['request']=request
        new_variables=variables
        return render_to_response(template, new_variables,context_instance=RequestContext(request))


# Consulta para saber los beneficiarios con sus detalles
def ConsulForm(request):
	bene = Persona.objects.all()
	query = request.GET.get('c', '')
	if query:
		results = Beneficiario.objects.filter(persona=query)
		return render_to_html(request,"/proyectos/resultado.html", {'results': results, 'bene':bene })
	else:
		return render_to_html(request,"/proyectos/resultado.html", {'bene':bene })

# Consulta para saber los detalles de las personas con sus detalles y proyectos a los que pertenece
def BeneficiarioView(request):
	F = BeneficiarioForm(request.GET)
	query = request.GET.get('beneficiarios', '')
	i = Persona.objects.all()
	if query:
		b = Persona.objects.filter(id=query)
		c = Beneficiario.objects.filter(persona__id=query)
		return render_to_html(request,"/proyectos/persona.html", {'F':F, 'b': b, 'c': c, 'i':i})
	else:
		
		return render_to_html(request,"/proyectos/persona.html", locals())

# Consulta sobre los datos de los proyectos
def ConsulProyecto(request):
	P = ProyectoForm(request.GET)
	query = request.GET.get('proyectos', '')
	k = Proyecto.objects.all()
	if query:
		j = Proyecto.objects.filter(id=query)
		ma = Beneficiario.objects.filter(proyecto__id=query)
		contar = ma.count()
		contmujer = Beneficiario.objects.filter(proyecto__id=query).filter(persona__sexo=0)
		mujer = contmujer.count()
		conthombre = Beneficiario.objects.filter(proyecto__id=query).filter(persona__sexo=1)
		hombre = conthombre.count()
		return render_to_html(request,"/proyectos/proyecto.html", {'P':P, 'j': j, 'contar': contar, 'mujer': mujer, 'hombre': hombre, 'ma': ma})
	else:
		
		return render_to_html(request,"/proyectos/proyecto.html", locals())

#Esto es solo prueba para saber si estaban bien los datos, todos los datos los tenemos en formato CSV 

