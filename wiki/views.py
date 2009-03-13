# -*- coding: utf-8 -*-
# Create your views here.
from wiki.models import Pagina
from coffin.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from urllib import quote_plus, unquote_plus
from wiki import models
from django.conf import settings
import unicodedata

index_menuitem = {'url' : '/wiki/', 'name' : 'Inicio'}
#index_menuitem = {'url' : '/wiki/'+str(settings.WIKI_STARTPAGE)+'/', 'name' : 'Inicio'}
list_menuitem = {'url' : '/wiki/list/', 'name' : 'Lista de p&aacute;ginas'}
estadisticas_menuitem = {'url' : '/estadisticas/', 'name' : 'Precios'}
#login_menuitem = {'url' : '/accounts/login/', 'name' : 'Login'}
#admin_menuitem = {'url' : '/admin/', 'name' : 'Administrar'}
menu_list = (index_menuitem, list_menuitem, estadisticas_menuitem)#, login_menuitem, admin_menuitem)


def render_to_html(request,template,variables):
	variables['request']=request
	new_variables=variables
        return render_to_response(template, new_variables,context_instance=RequestContext(request))


def list_page(request,javascript=False):
	all_pages = models.Pagina.objects.all()
	return render_to_html(request,"/list.html", {"all_pages":all_pages,"menu_list":menu_list})

def view_page(request, page_name,javascript=False):
	page_name=unquote_plus(page_name)
	try:
		page = Pagina.objects.get(nombre=page_name)
	except Pagina.DoesNotExist:
		if request.user.is_superuser:
			return HttpResponseRedirect("/admin/wiki/pagina/add/")
		else:
			content=page_name+" Desculpe, pero esta pagina ya no existe!"
			return render_to_html(request,"/view.html", {"page_name":page_name,"menu_list":menu_list,"content":content})			
	accented_page_name=page.nombre
	content	 = page.body_html()
	pk = page.pk
	if (request.user.has_perm('pagina.can_change')):
		can_change=True
	else:
		can_change=False
	return render_to_html(request,"/view.html", {"page_name":accented_page_name,"menu_list":menu_list,"content":content,"pk":pk,"can_change":can_change})



def search_page(request,javascript=False):
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string =	unicodedata.normalize('NFKD', unicode(request.GET['q'])).encode('ascii','ignore')
		found_entries = Pagina.index.search(query_string)
	return render_to_html(request,'/search_results.html',{ 'query_string': query_string, 'found_entries': found_entries, 'menu_list':menu_list })

