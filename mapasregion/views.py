# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from mapamagfor.mapa.models import Mapa

def lista_mapa(request):

    query= Mapa.objects.all()
    return render_to_response('mapa_list.html', {'mapa': query})
