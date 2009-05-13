# -*- coding: utf-8 -*-
from wiki.models import Pagina,Tag
from coffin.shortcuts import render_to_response
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


def list_page(request,tag_name=None):
	all_tags = Tag.objects.all()
	if tag_name!=None:
		all_pages=Pagina.objects.filter(tag__nombre__contains=tag_name)
	else: 
		all_pages = Pagina.objects.all()
	return render_to_html(request,"/list.html", {"all_pages":all_pages,"all_tags":all_tags})

def view_page(request, page_name):
	page_name=unquote_plus(page_name)
	try:
		page = Pagina.objects.get(nombre=page_name)
	except Pagina.DoesNotExist:
		if request.user.is_superuser:
			return HttpResponseRedirect("/admin/wiki/pagina/add/")
		else:
			content=page_name+" Desculpe, pero esta pagina ya no existe!"
			return render_to_html(request,"/view.html", {"page_name":page_name,"content":content})			
	accented_page_name=page.nombre
	body_html = page.body_html
	json_data = page.json_data
	pk = page.pk
	if (request.user.has_perm('pagina.can_change')):
		can_change=True
	else:
		can_change=False
	return render_to_html(request,"/view.html", {"page_name":accented_page_name,"body_html":body_html,"json_data":json_data,"pk":pk,"can_change":can_change})



def search_page(request, search_term=None):
	if search_term!=None:
		found_entries = Pagina.index.search(search_term)
		return render_to_html(request,'/search_results.html',{ 'query_string': search_term, 'found_entries': found_entries })
	else:
		return render_to_html(request,'/search_form.html',{ })


def search_page_html(request):
	if ('q' in request.GET) and request.GET['q'].strip():
		search_term = request.GET['q']
		return HttpResponseRedirect("/busqueda/"+search_term+"/")
	else:
		return HttpResponseRedirect("/busqueda/")
