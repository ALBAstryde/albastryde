# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from mapamagfor.mapa.models import Mapa, Tipo

def index_mapa(request):
    tipo = Tipo.objects.all()
    return render_to_response('index_mapa.html',{'tipo': tipo})

def lista_mapa(request, t):
    tipo = Tipo.objects.all()
    query= Mapa.objects.filter(tipo=t)
    t = Tipo.objects.get(pk=t)
    return render_to_response('mapa_list.html', {'mapa': query, 'tipo': tipo, 't':t})

def lista_mapa_region(request, r):
    tipo = Tipo.objects.all()
    query= Mapa.objects.filter(region=r)
    reg=""
    if r == "1":
        reg="Region Pacifico Norte"
    if r == "2":
        reg="Region Pacifico Central"
    if r == "3":
        reg="Region Pacifico Sur"
    if r == "4":
        reg="Region Las Segovias"
    if r == "5":
        reg="Region Central Norte"
    if r == "6":
        reg="Region Central Este"
    if r == "7":
        reg="Region Caribe Norte(RAAN)"
    if r == "8":
        reg="Region Caribe Sur(RAAS)"
    if r == "9":
        reg="Region del Rio San Juan"
    return render_to_response('mapa_list_region.html', {'mapa': query, 'tipo': tipo,'reg':reg})
