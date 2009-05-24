from precios.models import Prueba as PrecioPrueba
from precios.models import Mercado
from lluvia.models import Prueba as LLuviaPrueba
from graph.forms import DbForm
from valuta.models import USD,Euro
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from datetime import date
from time import mktime


def build_graph(query,user):
	form = DbForm(query)
        clean=form.is_valid()# Make some dicts to get passed back to the browser
        rdict = {'bad':'false'}
        if not clean:
        	rdict.update({'bad':'true'})
                d={}
                # extract the error messages:
                for e in form.errors.iteritems():
                	d.update({e[0]:unicode(e[1])}) # e[0] is the id, unicode(e[1]) is the error HTML.
                        # Bung all that into the dict
                rdict.update({'errs': d  })
       	else:   
		last_date=date(1920,1,1).timetuple()
		first_date=date.today().timetuple()
		pk_list=[]
		graphs=[]
		municipios = form.cleaned_data['Municipio']
		departamentos = form.cleaned_data['Departamento']
		mercados_queryset = form.cleaned_data['Mercado']
		mercados=[]
		for i in mercados_queryset:
			mercados.append(i)
		productos = form.cleaned_data['Producto']
		frequencies = form.cleaned_data['Frequency']
		estaciones_de_lluvia_queryset = form.cleaned_data['EstacionDeLluvia']
		estaciones_de_lluvia=[]
		for i in estaciones_de_lluvia_queryset:
			estaciones_de_lluvia.append(i)
		include_lluvia = form.cleaned_data['IncluirLluvia']
		start_date = form.cleaned_data['Desde']
		end_date = form.cleaned_data['Hasta']
		producto_count=len(productos)
		municipio_count=len(municipios)
		departamento_count=len(departamentos)
		if producto_count > 0:		
			if municipio_count > 0:
				for municipio in municipios:
					if len(municipio.mercado_set.all()) > 0:
						for i in municipio.mercado_set.all().iterator():
							mercados.append(i)
			if departamento_count > 0:
				for departamento in departamentos:
					for municipio in departamento.municipios.iterator():
						if len(municipio.mercado_set.all()) > 0:
							for i in municipio.mercado_set.all().iterator():
								mercados.append(i)
		mercado_count=len(mercados)
		if include_lluvia:
			if municipio_count > 0:
				for municipio in municipios:
					for i in municipio.estaciondelluvia_set.all().iterator():
						estaciones_de_lluvia.append(i)
			if departamento_count > 0:
				for departamento in departamentos:
					for municipio in departamento.municipios.iterator():
						for i in municipio.estaciondelluvia_set.all().iterator():
							estaciones_de_lluvia.append(i)
		lluvia_count=len(estaciones_de_lluvia)
		if mercado_count > 0 and producto_count > 0:
			dollar={'unit':'USD','monthly':{},'annualy':{},'daily':{}}
			euro={'unit':'Euro','monthly':{},'annualy':{},'daily':{}}
		pricectype = ContentType.objects.get(app_label__exact='precios', name__exact='prueba')
		lluviactype = ContentType.objects.get(app_label__exact='lluvia', name__exact='prueba')
		for frequency in frequencies:
			for i in mercados:
				for b in productos:
					graph,dollar,euro,pk_list,first_date,last_date=price_graph(mercado=i,producto=b,frequency=frequency,start_date=start_date,end_date=end_date,mercado_count=mercado_count,producto_count=producto_count,dollar=dollar,euro=euro,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=pricectype)
					if not graph==None:
						graphs.append(graph)
			for d in estaciones_de_lluvia:
				graph,pk_list,first_date,last_date=lluvia_graph(estacion=d,frequency=frequency,start_date=start_date,end_date=end_date,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=lluviactype)
				if not graph==None:
					graphs.append(graph)							
		rdict.update({'graphs':graphs})
		mercado_name=""
		lluvia_name=""
		producto_name=""
		precio_name=""
		if mercado_count > 0 and producto_count > 0:
			rdict.update({'dollar':dollar})
			rdict.update({'euro':euro})
			for i in mercados:
				mercado_name+=i.nombre+", "
			mercado_name=mercado_name.strip(", ")
			if len(mercado_name)>60:
				mercado_name="el mercado"
			for i in productos:
				producto_name+=i.nombre.title()+", "
			producto_name=producto_name.strip(", ")
			if len(producto_name)>60:
				producto_name="Unos productos"
			precio_name=producto_name+" en "+mercado_name 
		if lluvia_count > 0:
			for i in estaciones_de_lluvia:
				lluvia_name+=i.nombre.title()+", "
			lluvia_name=lluvia_name.strip(", ")
		headline=""
		if precio_name != "" and lluvia_name !="":
			headline += "Precios "
			headline += precio_name
			headline += " y lluvia en "				
			headline +=lluvia_name
		elif lluvia_name !="":
			headline +="Lluvia en "
			headline +=lluvia_name
		elif precio_name !="":
			headline +="Precios "
			headline +=precio_name
				
		headline+=": "+str(date.fromtimestamp(mktime(first_date)))+"&ndash;"+str(date.fromtimestamp(mktime(last_date)))
		rdict.update({'headline':headline})
		comments={}
		for content_type in pk_list :
	               	all_comments_qs=Comment.objects.filter(content_type=content_type[0], object_pk__in=content_type[1],is_removed=False)
			if (user.has_perm('comments.can_manage')):
				comments_qs = all_comments_qs
			elif (user.is_authenticated()):
				my_comments_qs=all_comments_qs.filter(user=user)
				public_comments_qs=all_comments_qs.filter(is_public=True)	
				comments_qs= my_comments_qs | public_comments_qs
			else:
				comments_qs=all_comments_qs.filter(is_public=True)	
			if len(comments_qs)>0:
				for i in comments_qs:
					unique_pk=str(content_type[0])+"_"+str(i.object_pk)
					if not unique_pk in comments:
						comments[unique_pk]={}
					if (user.has_perm('comments.can_manage') or (i.user==user and user.has_perm('comments.change_comment'))):
						puede_editar=True
					else:
						puede_editar=False
					comments[unique_pk][i.pk]=[i.comment,i.name,puede_editar,i.is_public]
				rdict.update({'comments':comments})
	return rdict

from django.db import connection

def price_graph(mercado,producto,frequency,start_date,end_date,mercado_count,producto_count,dollar,euro,pk_list,first_date,last_date,ctype):
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

