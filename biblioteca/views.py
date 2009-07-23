 # -*- coding: UTF-8 -*-

from django.conf import settings 
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse 
from django.shortcuts import render_to_response
from models import Biblioteca
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import os 

def search(request):
	count = 0
	a = Biblioteca.objects.order_by('-fecha')[:5]
	query = request.GET.get('q', '')
	query = query.replace(",","")
	if query:
		qset = (
			Q(palabra_clave__icontains=query)
				)
		results = Biblioteca.objects.filter(qset).distinct()
		for b in results:
			count += 1
	else:
		results = []
	return render_to_response("index.html", {
        "results": results,
        "query": query,
        "a": a,
        "c": count
    },
    context_instance = RequestContext(request))
    
def detalle(request, libro):
	a = Biblioteca.objects.order_by('-fecha')[:5]
	resultado = Biblioteca.objects.get(id=libro)
	return render_to_response("detalle.html", {
        "results": resultado,
        "a": a
    })
       
def handles_uploaded_file(f):
	file_name = os.path.join(settings.ATTACHMENT_PATH, f.name)
	destination = open(file_name, 'wb+')
	for chunk in f.chunk():
		destination.write(chunk)
	destination.close()
