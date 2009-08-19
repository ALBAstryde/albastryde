# -*- coding: utf-8 -*-

from django.conf import settings

def site_theme(request):
	return {'site_theme': settings.SITE_THEME}

def site_language(request):
	return {'site_language': settings.SITE_LANGUAGE}

def menu_list(request):
	index_menuitem = {'url' : '/wiki/', 'name' : 'Wiki'}
	list_menuitem = {'url' : '/list/', 'name' : 'Lista de p&aacute;ginas'}
	estadisticas_menuitem = {'url' : '/estadisticas/', 'name' : 'Estad&iacute;sticas'}
	biblioteca_menuitem = {'url' : '/biblioteca/', 'name' : 'Biblioteca'}
	proyectos_menuitem = {'url' : '/proyectos/', 'name' : 'Proyectos'}
	cooperativas_menuitem = {'url' : '/cooperativas/', 'name' : 'Cooperativas'}
	mapas_menuitem = {'url' : '/mapas/', 'name' : 'Mapas'}
	busqueda_menuitem = {'url' : '/busqueda/', 'name' : 'Buscar'}
	menu_list = (index_menuitem, list_menuitem, estadisticas_menuitem, biblioteca_menuitem, proyectos_menuitem, cooperativas_menuitem, mapas_menuitem, busqueda_menuitem)
	return {'menu_list':menu_list}



def compress(request):
	return_dic={}
	if settings.COMPRESS_JS:
		for javascript_group in settings.COMPRESS_JS.iterkeys():
			if settings.DEBUG==False:
				return_dic['compressed_js_'+javascript_group]='<script type="text/javascript" src="'+settings.MEDIA_URL+settings.COMPRESS_JS[javascript_group]['output_filename']+'" charset="utf-8"></script>'	
			else:
				return_dic['compressed_js_'+javascript_group]=''
				for javascript_file in settings.COMPRESS_JS[javascript_group]['source_filenames']:
					return_dic['compressed_js_'+javascript_group]+='<script type="text/javascript" src="'+settings.MEDIA_URL+javascript_file+'" charset="utf-8"></script>'
	if settings.COMPRESS_CSS:
		for css_group in settings.COMPRESS_CSS.iterkeys():
			if settings.DEBUG==False:
				return_dic['compressed_css_'+css_group]='<link href="'+settings.MEDIA_URL+settings.COMPRESS_CSS[css_group]['output_filename']+'" rel="stylesheet" type="text/css">'	
			else:
				return_dic['compressed_css_'+css_group]=''
				for css_file in settings.COMPRESS_CSS[css_group]['source_filenames']:
					return_dic['compressed_css_'+css_group]+='<link href="'+settings.MEDIA_URL+css_file+'" rel="stylesheet" type="text/css">'

	return return_dic
