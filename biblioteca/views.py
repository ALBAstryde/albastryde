 # -*- coding: UTF-8 -*-

from wiki.models import Pagina,Tag
from coffin.shortcuts import render_to_response
from django.conf import settings 
from django.template import RequestContext
from biblioteca.models import Documento,PalabraClave

def render_to_html(request,template,variables):
        variables['request']=request
        new_variables=variables
        return render_to_response(template, new_variables,context_instance=RequestContext(request))


def palabra_clave(request,pk):
	all_palabras_claves=PalabraClave.objects.all()	
	a = Documento.objects.order_by('-fecha_anadido')[:5]
	palabra_clave=PalabraClave.objects.get(pk=pk)
	documentos=palabra_clave.documento_set.all()
        return render_to_html(request,"/biblioteca/biblioteca_palabra_clave.html", {
			"palabra_clave": palabra_clave,
			"all_palabras_claves": all_palabras_claves,
			"documentos": documentos,
			"a": a,
		}
	)

def index(request):
	all_palabras_claves=PalabraClave.objects.all()	
	a = Documento.objects.order_by('-fecha_anadido')[:5]
        return render_to_html(request,"/biblioteca/biblioteca.html", {
			"all_palabras_claves": all_palabras_claves,
        		"a": a
		}
	)
    
def detalle(request, libro):
	all_palabras_claves=PalabraClave.objects.all()	
	a = Documento.objects.order_by('-fecha_anadido')[:5]
	resultado = Documento.objects.get(pk=libro)
	return render_to_html(request,"/biblioteca/biblioteca_detalle.html", {
		"all_palabras_claves": all_palabras_claves,
	       	"results": resultado,
        	"a": a
	})
       
