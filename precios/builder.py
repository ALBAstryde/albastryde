from precios.models import Prueba as PrecioPrueba
#from precios.models import Mercado
from valuta.models import USD,Euro
#from datetime import date
from time import mktime
from django.db import connection

def precio_graph(mercado,producto,frequency,start_date,end_date,mercado_count,producto_count,dollar,euro,pk_list,first_date,last_date,ctype):
	queryset = None
	if frequency=='daily':
		queryset = PrecioPrueba.objects.filter(producto=producto,mercado=mercado,fecha__range=[start_date,end_date]).values('fecha','pk','maximo','minimo').order_by('fecha')
	else:
		cursor = connection.cursor()
		if frequency=='monthly':
			cursor.execute("select producto_id as producto, mercado_id as mercado, date_trunc('month',fecha) as fecha, avg(maximo) as maximo, avg(minimo) as minimo from precios_prueba where producto_id = "+str(producto.pk)+" and mercado_id = "+str(mercado.pk)+" and fecha > '"+start_date.strftime('%Y-%m-%d')+"' and fecha < '"+end_date.strftime('%Y-%m-%d')+"' group by date_trunc('month',fecha), producto_id, mercado_id order by fecha;")
		elif frequency=='annualy':
			cursor.execute("select producto_id as producto, mercado_id as mercado, date_trunc('year',fecha) as fecha, avg(maximo) as maximo, avg(minimo) as minimo from precios_prueba where producto_id = "+str(producto.pk)+" and mercado_id = "+str(mercado.pk)+" and fecha > '"+start_date.strftime('%Y-%m-%d')+"' and fecha < '"+end_date.strftime('%Y-%m-%d')+"' group by date_trunc('year',fecha), producto_id, mercado_id order by fecha;")
		queryset=[]
		for row in cursor.fetchall():
			row_dic={'fecha':row[2],'maximo':row[3],'minimo':row[4],'producto':row[0],'mercado':row[1]}
			queryset.append(row_dic)
	content_type=ctype.id
	if len(queryset)==0:
		return None,dollar,euro,pk_list,first_date,last_date
	max_data=[]
	min_data_dic={}
	list_of_pk=[]
	for i in queryset:
		if i['fecha'].timetuple() < first_date:
			first_date=i['fecha'].timetuple()
		if i['fecha'].timetuple() > last_date:
			last_date=i['fecha'].timetuple()
		fecha=mktime(i['fecha'].timetuple())
		adjusted_fecha=fecha
		if frequency=='daily':
			adjusted_fecha+=22000
		elif frequency=='monthly':
			adjusted_fecha+=1365000
		elif frequency=='annualy':
			adjusted_fecha+=15800000
		precio=int(i['maximo'])		
		if i['maximo'] != i['minimo']:
			min_data_dic[int(adjusted_fecha)]=int(i['minimo'])
		if not str(int(adjusted_fecha)) in dollar[frequency]:
			if frequency=='daily':
				dollar[frequency][str(int(adjusted_fecha))]=float(USD.objects.get(fecha__exact=i['fecha']).cordobas)
				euro[frequency][str(int(adjusted_fecha))]=float(Euro.objects.get(fecha__exact=i['fecha']).cordobas)
			else:
				cursor = connection.cursor()
				if frequency=='monthly':
					cursor.execute("select avg(cordobas) from valuta_usd where date_trunc('month',fecha)='"+i['fecha'].strftime('%Y-%m-%d')+"';")
				elif frequency=='annualy':
					cursor.execute("select avg(cordobas) from valuta_usd where date_trunc('year',fecha)='"+i['fecha'].strftime('%Y-%m-%d')+"';")
				dollar[frequency][str(int(adjusted_fecha))]= float(cursor.fetchone()[0])
				if frequency=='monthly':
					cursor.execute("select avg(cordobas) from valuta_euro where date_trunc('month',fecha)='"+i['fecha'].strftime('%Y-%m-%d')+"';")
				elif frequency=='annualy':
					cursor.execute("select avg(cordobas) from valuta_euro where date_trunc('year',fecha)='"+i['fecha'].strftime('%Y-%m-%d')+"';")
				euro[frequency][str(int(adjusted_fecha))]= float(cursor.fetchone()[0])				
		adjusted_fecha=int(adjusted_fecha)
		if frequency=='daily':
			unique_pk=str(content_type)+"_"+str(i['pk'])		
			list_of_pk.append(str(i['pk']))
			max_data.append([adjusted_fecha,precio,unique_pk])
		else:
			max_data.append([adjusted_fecha,precio])
	if frequency=='daily':
		pk_list.append([content_type,list_of_pk])
	result={'included_variables':{'producto':producto.nombre,'mercado':mercado.nombre},'unit':'cordoba','type':'precio','frequency':frequency,'main_variable_js':'this.included_variables.producto','place_js':'this.included_variables.mercado','normalize_factor_js':'this.start_value','display':'lines'}
	if len(min_data_dic)==0:
		result['data']=max_data
	else:
		result['max_data']=max_data
		result['min_data_dic']=min_data_dic
	return result,dollar,euro,pk_list,first_date,last_date

