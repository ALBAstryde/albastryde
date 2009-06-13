# -*- coding: utf-8 -*-
from datetime import date
from time import mktime
from cosecha.models import Cosecha
#from django.db import connection
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum


content_type = ContentType.objects.get(app_label__exact='cosecha', name__exact='cosecha').id

def cosecha_builder(form_data,frequencies):
	# Recogiendo datos del formulario, mas es campo frecuencias, ya truducido a ingles
	departamentos = form_data['Departamento']
	municipios = form_data['Municipio']
	cosecha_variable = form_data['CosechaVariable']
	cosecha_producto = form_data['CosechaProducto']
	start_date = form_data['Desde']
	end_date = form_data['Hasta']


	if 'annualy' in frequencies:
		if len(frequencies)>1:
			frequencies=['monthly','annualy']
		else:
			frequencies=['annualy']
	else:
		frequencies=['monthly']



# juntar todos los municipios de cada uno de los departamentos seleccionados con la lista de muncipios selecionados directamente
#	for departamento in departamentos:
#		if len(departamento.municipios.all()) > 0:
#			if len(municipios) > 0:
#				municipios = municipios | departamento.municipios.all()
#			else:
#				municipios = departamento.municipios.all()

	pk_list=[]
	graphs=[]
	
	# Aqui se llama la funcion para hacer cada uno de los graficos
	for frequency in frequencies:
		for d in cosecha_variable:
			for i in cosecha_producto:
				for e in municipios:
					graph,pk_list=cosecha_graph(variable=d,municipio=e,producto=i,start_date=start_date,end_date=end_date,pk_list=pk_list,frequency=frequency)
					if not graph==None:
						graphs.append(graph)	
				for f in departamentos:
					graph,pk_list=cosecha_graph(variable=d,departamento=f,producto=i,start_date=start_date,end_date=end_date,pk_list=pk_list,frequency=frequency)
					if not graph==None:
						graphs.append(graph)	
	return graphs,pk_list
# Esta es para traducir las fechas de los tiempos
def traducir_fecha(date):
	cosecha_tiempo={}
	if date.month < 3:
		cosecha_tiempo['ano']=date.year-1
		cosecha_tiempo['tiempo']=3
	elif date.month > 2 and date.month < 6:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=1
	elif date.month > 5 and date.month < 9:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=2
	elif date.month > 8:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=3
	return cosecha_tiempo

def traducir_tiempo(ano,tiempo):
	if tiempo==1:
		return date(year=ano,month=3,day=1)
	elif tiempo==2:
		return date(year=ano,month=6,day=1)
	elif tiempo==3:
		return date(year=ano,month=9,day=1)
	return None

def variable_converter(variable):
	composed=False
	if variable=='area estimada':
		value='area_estimada'
		unit= 'mz'
	elif variable=='producto estimado':
		value='producto_estimado'
		unit='qq'
	elif variable=='area sembrada':
		value='area_sembrada'
		unit='mz'
	elif variable=='area cosechada':
		value='area_cosechada'
		unit='mz'
	elif variable=='producto obtenido':
		value='producto_obtenido'
		unit='qq'
	elif variable=='rendimiento estimado':
		value=['producto_estimado','area_estimada','/']
		composed=True
		unit='qq/mz'
	elif variable=='rendimiento obtenido':
		value=['producto_obtenido','area_cosechada','/']
		composed=True
		unit='qq/mz'
	elif variable=='area perdida':
		value='area_perdida'
		unit='mz'
	else:
		value='0'
		unit=''
	return value,unit,composed
	
def cosecha_graph(variable,producto,start_date,end_date,pk_list,frequency,departamento=None,municipio=None):
	cosecha_start=traducir_fecha(start_date)
	cosecha_end=traducir_fecha(end_date)
	a=Cosecha.objects.filter(ano=cosecha_start['ano']).filter(tiempo__gt= cosecha_start['tiempo']-1).filter(producto=producto)
	b=Cosecha.objects.filter(ano__gt=cosecha_start['ano']).filter(ano__lt=cosecha_end['ano']).filter(producto=producto)
	c=Cosecha.objects.filter(ano=cosecha_end['ano']).filter(tiempo__lt=cosecha_end['tiempo']+1).filter(producto=producto)
	basic_queryset=a|b|c
	if departamento:
		geo_situated_queryset=basic_queryset.filter(municipio__departamento=departamento)
		if frequency=='annualy':
			valued_queryset = geo_situated_queryset.values('ano')
		else:
			valued_queryset = geo_situated_queryset.values('ano','tiempo')
	else:
		geo_situated_queryset=basic_queryset.filter(municipio=municipio)
		if frequency=='annualy':
			valued_queryset = geo_situated_queryset.values('ano')
		else:
			valued_queryset = geo_situated_queryset.values('ano','tiempo','pk')
	value_name,unit,composed=variable_converter(variable)
	if composed:
		queryset = valued_queryset.annotate(Sum(value_name[0]),Sum(value_name[1]))
	else:
		queryset = valued_queryset.annotate(Sum(value_name))

	if len(queryset)==0:
		return None,pk_list
	data=[]
	list_of_pk=[]
	for i in queryset:
		if frequency=='annualy':
			fecha=int(mktime(traducir_tiempo(ano=i['ano'],tiempo=1).timetuple()))
			to_fecha=int(mktime(traducir_tiempo(ano=i['ano']+1,tiempo=1).timetuple())-1)
		else:
			fecha=int(mktime(traducir_tiempo(ano=i['ano'],tiempo=i['tiempo']).timetuple()))
			if i['tiempo']==3:
				to_tiempo=1
				to_ano=i['ano']+1
			else:
				to_tiempo=i['tiempo']+1
				to_ano=i['ano']
			to_fecha=int(mktime(traducir_tiempo(ano=to_ano,tiempo=to_tiempo).timetuple())-1)
		if composed:
			if i[value_name[0]+'__sum']==0 or i[value_name[1]+'__sum']==0:
				value=0
			else:
				value=i[value_name[0]+'__sum']/i[value_name[1]+'__sum']
		else:
			value=i[value_name+'__sum']
		if municipio and frequency=='monthly':
			unique_pk=str(content_type)+"_"+str(i['pk'])
			list_of_pk.append(str(i['pk']))
			data.append([[fecha,to_fecha],value,unique_pk])
			pk_list.append([content_type,list_of_pk])
			source='raw'
		else:
			data.append([[fecha,to_fecha],value])
			source='computed'
	if departamento:
		included_variables={'departamento':departamento.nombre, 'producto':producto.nombre}
		place_js='new_graph.included_variables.departamento'
	else:
		included_variables={'municipio':municipio.nombre, 'producto':producto.nombre}
		place_js='new_graph.included_variables.municipio'
	result = {'included_variables':included_variables,'data':data,'source':source,'unit':unit,'type':variable,'frequency':frequency,'main_variable_js':'new_graph.type+" de "+new_graph.included_variables.producto','place_js':place_js,'normalize_factor_js':'new_graph.start_value','display':'bars'}
	return result,pk_list

