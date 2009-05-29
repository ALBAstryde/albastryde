# -*- coding: utf-8 -*-
from lluvia.models import Prueba as LLuviaPrueba
#from datetime import date
from time import mktime
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from precios.builder import add_month, add_year

content_type = ContentType.objects.get(app_label__exact='lluvia', name__exact='prueba').id

def lluvia_builder(form_data,frequencies):
  		pk_list=[]
		graphs=[]
		municipios = form_data['Municipio']
		departamentos = form_data['Departamento']
		estaciones = form_data['EstacionDeLluvia']
		include_lluvia = form_data['IncluirLluvia']
		start_date = form_data['Desde']
		end_date = form_data['Hasta']
		for departamento in departamentos:
		  	if len(departamento.municipios.all()) > 0:
			  	if len(municipios) > 0:
					municipios = municipios | departamento.municipios.all()
				else:
				  	municipios = departamento.municipios.all()
		if include_lluvia:
			for municipio in municipios:
			  	if len(municipio.estaciondelluvia_set.all()) > 0:
				  	if len(estaciones) > 0:
						estaciones = estaciones | municipio.estaciondelluvia_set.all()
					else:
					  	estaciones = municipio.estaciondelluvia_set.all()

		# Aqui se llaman las funciones para hacer cada uno de los graficos

		for frequency in frequencies:
			for d in estaciones:
				graph,pk_list=lluvia_graph(estacion=d,frequency=frequency,start_date=start_date,end_date=end_date,pk_list=pk_list)
				if not graph==None:
					graphs.append(graph)
					
		return graphs,pk_list

def lluvia_graph(estacion,frequency,start_date,end_date,pk_list):
	queryset = None
	if frequency=='daily':
		queryset =LLuviaPrueba.objects.filter(estacion=estacion).filter(fecha__range=[start_date,end_date]).values('fecha','pk','milimetros_de_lluvia').order_by('fecha')
		source='raw'
	else:
		cursor = connection.cursor()
		if frequency=='monthly':
			cursor.execute("select estacion_id as estacion, date_trunc('month',fecha) as fecha, avg(milimetros_de_lluvia) as milimetros_de_lluvia from lluvia_prueba where estacion_id = "+str(estacion.pk)+" and fecha > '"+start_date.strftime('%Y-%m-%d')+"' and fecha < '"+end_date.strftime('%Y-%m-%d')+"' group by date_trunc('month',fecha), estacion_id order by fecha;")
		elif frequency=='annualy':
			cursor.execute("select estacion_id as estacion, date_trunc('year',fecha) as fecha, avg(milimetros_de_lluvia) as milimetros_de_lluvia from lluvia_prueba where estacion_id = "+str(estacion.pk)+" and fecha > '"+start_date.strftime('%Y-%m-%d')+"' and fecha < '"+end_date.strftime('%Y-%m-%d')+"' group by date_trunc('year',fecha), estacion_id order by fecha;")
		queryset=[]
		for row in cursor.fetchall():
			row_dic={'fecha':row[1],'milimetros_de_lluvia':row[2],'estacion':row[0]}
			queryset.append(row_dic)
		source='computed'
	if len(queryset)==0:
		return None,pk_list
	data=[]
	list_of_pk=[]
	for i in queryset:
		if i['milimetros_de_lluvia'] > 0:
			value=str(i['milimetros_de_lluvia'])
			fecha=i['fecha']
                	now_fecha=mktime(fecha.timetuple())
                	if frequency=='daily':
                        	next_fecha=now_fecha+86399
                	elif frequency=='monthly':
                        	next_fecha=mktime(add_month(fecha).timetuple())-1
                	elif frequency=='annualy':
                        	next_fecha=mktime(add_year(fecha).timetuple())-1
                	else:
                        	next_fecha=now_fecha
			now_fecha=int(now_fecha)
			next_fecha=int(next_fecha)
			if frequency=='daily':
				unique_pk=str(content_type)+"_"+str(i['pk'])		
				list_of_pk.append(str(i['pk']))
				data.append([[now_fecha,next_fecha],value,unique_pk])
			else:
				data.append([[now_fecha,next_fecha],value])
	if frequency=='daily':
		pk_list.append([content_type,list_of_pk])
	result={'included_variables':{'station':estacion.nombre},'data':data,'unit':'mm','type':'lluvia','source':source,'frequency':frequency,'main_variable_js':'"lluvia"','place_js':'this.included_variables.station','normalize_factor_js':'this.top_value','display':'bars'}
	return result,pk_list
