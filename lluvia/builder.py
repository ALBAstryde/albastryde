from lluvia.models import Prueba as LLuviaPrueba
#from datetime import date
from time import mktime
from django.db import connection

def lluvia_graph(estacion,frequency,start_date,end_date,pk_list,first_date,last_date,ctype):
	queryset = None
	if frequency=='daily':
		queryset =LLuviaPrueba.objects.filter(estacion=estacion).filter(fecha__range=[start_date,end_date]).values('fecha','pk','milimetros_de_lluvia').order_by('fecha')
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
	content_type=ctype.id
	if len(queryset)==0:
		return None,pk_list,first_date,last_date
	data=[]
	list_of_pk=[]
	for i in queryset:
		if i['milimetros_de_lluvia'] > 0:
			if i['fecha'].timetuple() < first_date:
				first_date=i['fecha'].timetuple()
			if i['fecha'].timetuple() > last_date:
				last_date=i['fecha'].timetuple()
			value=str(i['milimetros_de_lluvia'])
			fecha=mktime(i['fecha'].timetuple())
			fecha=int(fecha)
			if frequency=='daily':
				unique_pk=str(content_type)+"_"+str(i['pk'])		
				list_of_pk.append(str(i['pk']))
				data.append([fecha,value,unique_pk])
			else:
				data.append([fecha,value])
	if frequency=='daily':
		pk_list.append([content_type,list_of_pk])
	result={'included_variables':{'station':estacion.nombre},'data':data,'unit':'mm','type':'lluvia','frequency':frequency,'main_variable_js':'"lluvia"','place_js':'this.included_variables.station','normalize_factor_js':'this.top_value','display':'bars'}
	return result,pk_list,first_date,last_date
