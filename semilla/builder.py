# -*- coding: utf-8 -*-
from datetime import date
from time import mktime
from semilla.models import Semilla, CATEGORIA_CHOICES
#from django.db import connection
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum


content_type = ContentType.objects.get(app_label__exact='semilla', name__exact='semilla').id

def semilla_builder(form_data,frequencies):
	# Recogiendo datos del formulario, mas es campo frecuencias, ya truducido a ingles
	departamentos = form_data['LugarDepartamento']
	semilla_categoria = form_data['SemillaCategoria']
	semilla_producto = form_data['SemillaProducto']
	semilla_variedad = form_data['SemillaVariedad']
	start_date = form_data['Desde']
	end_date = form_data['Hasta']


	if 'annualy' in frequencies:
		if len(frequencies)>1:
			frequencies=['monthly','annualy']
		else:
			frequencies=['annualy']
	else:
		frequencies=['monthly']



	pk_list=[]
	graphs=[]
	
	# Aqui se llama la funcion para hacer cada uno de los graficos
	for frequency in frequencies:
		for d in semilla_categoria:
			for e in departamentos:
				for f in semilla_producto:
					graph,pk_list=semilla_graph(categoria=d,departamento=e,producto=f,start_date=start_date,end_date=end_date,pk_list=pk_list,frequency=frequency)
					if not graph==None:
						graphs.append(graph)	
				for g in semilla_variedad:
					graph,pk_list=semilla_graph(categoria=d,departamento=e,variedad=g,start_date=start_date,end_date=end_date,pk_list=pk_list,frequency=frequency)
					if not graph==None:
						graphs.append(graph)	
	return graphs,pk_list
# Esta es para traducir las fechas de los tiempos
def traducir_fecha(date):
	semilla_tiempo={}
	semilla_tiempo['ano']=date.year
	semilla_tiempo['mes']=date.month
	return semilla_tiempo

def traducir_tiempo(ano,mes):
	return date(year=ano,month=mes,day=1)

def pick_categoria_name(categoria):
	for i in CATEGORIA_CHOICES:
		if str(i[0])==str(categoria):
			return i[1]
	return ''

def semilla_graph(categoria,departamento,start_date,end_date,pk_list,frequency,variedad=None,producto=None):
	semilla_start=traducir_fecha(start_date)
	semilla_end=traducir_fecha(end_date)
	a=Semilla.objects.filter(ano=semilla_start['ano']).filter(mes__gt= semilla_start['mes']-1).filter(categoria=categoria).filter(productor__departamento=departamento)
	b=Semilla.objects.filter(ano__gt=semilla_start['ano']).filter(ano__lt=semilla_end['ano']).filter(categoria=categoria).filter(productor__departamento=departamento)
	c=Semilla.objects.filter(ano=semilla_end['ano']).filter(mes__lt=semilla_end['mes']+1).filter(categoria=categoria).filter(productor__departamento=departamento)
	basic_queryset=a|b|c
	if producto:
		basic_queryset=basic_queryset.filter(variedad__producto=producto)
	elif variedad:
		basic_queryset=basic_queryset.filter(variedad=variedad)
	if frequency=='annualy':
		valued_queryset = basic_queryset.values('ano')
	else:
		valued_queryset = basic_queryset.values('ano','mes')
	queryset = valued_queryset.annotate(Sum('cantidad'))

	if len(queryset)==0:
		return None,pk_list
	data=[]
	list_of_pk=[]
	for i in queryset:
		if frequency=='annualy':
			fecha=int(mktime(traducir_tiempo(ano=i['ano'],mes=1).timetuple()))
			to_fecha=int(mktime(traducir_tiempo(ano=i['ano']+1,mes=1).timetuple())-1)
		else:
			fecha=int(mktime(traducir_tiempo(ano=i['ano'],mes=i['mes']).timetuple()))
			if i['mes']==12:
				to_mes=1
				to_ano=i['ano']+1
			else:
				to_mes=i['mes']+1
				to_ano=i['ano']
			to_fecha=int(mktime(traducir_tiempo(ano=to_ano,mes=to_mes).timetuple())-1)
		value=float(i['cantidad__sum'])
		data.append([[fecha,to_fecha],value])
		source='computed'
	included_variables={'departamento':departamento.nombre,'categoria':pick_categoria_name(categoria)}
	if producto:
		included_variables['producto']=producto.nombre
		main_variable_js='"semilla de "+new_graph.included_variables.producto+" "+new_graph.included_variables.categoria'
	elif variedad:
		included_variables['variedad']=variedad.__unicode__()
		main_variable_js='"semilla de "+new_graph.included_variables.variedad+" "+new_graph.included_variables.categoria'
	place_js='new_graph.included_variables.departamento'
	result = {'included_variables':included_variables,'data':data,'source':source,'unit':'qq','type':'semilla','frequency':frequency,'main_variable_js':main_variable_js,'place_js':place_js,'normalize_factor_js':'new_graph.start_value','display':'bars'}
	return result,pk_list

