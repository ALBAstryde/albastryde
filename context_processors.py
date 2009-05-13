from django.conf import settings

def site_theme(request):
	return {'site_theme': settings.SITE_THEME}

def menu_list(request):
	index_menuitem = {'url' : '/wiki/', 'name' : 'Wiki'}
	list_menuitem = {'url' : '/list/', 'name' : 'Lista de p&aacute;ginas'}
	estadisticas_menuitem = {'url' : '/estadisticas/', 'name' : 'Estad&iacute;sticas'}
	busqueda_menuitem = {'url' : '/busqueda/', 'name' : 'Buscar'}
	menu_list = (index_menuitem, list_menuitem, estadisticas_menuitem, busqueda_menuitem)
	return {'menu_list':menu_list}

