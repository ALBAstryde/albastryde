from precios.models import Prueba as PrecioPrueba
from lluvia.models import Prueba as LLuviaPrueba
from graph.forms import DbForm
from valuta.models import USD,Euro
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.db.models.options import get_verbose_name

import operator
import itertools
import pprint
import datetime
from time import mktime
from django.http import QueryDict

def camelcase(string):
	decamelcase_list= string.strip().split()
	camelcase_string=''
	for j in decamelcase_list:
		camelcase_string+=j.capitalize()
	return camelcase_string


def translate_query_string(query_string):
	word_query=QueryDict(query_string)
	new_query_string=u''
	for i in word_query.lists():
		modelname=i[0].strip().lower()
		values= i[1]
		if modelname==u'desde':
			modelname=u'start date'
		if modelname==u'hasta':
			modelname=u'end date'
		if modelname==u'start date' or modelname==u'end date' or modelname==u'frecuencia':
			new_query_string+="&"+camelcase(modelname)+"="+values[0]
		else:
			ctype_list = ContentType.objects.filter(name=modelname)
			if len(ctype_list) > 0:
				ctype=ctype_list[0]
				if len(ctype_list) > 1:
					name_length=len(ctype.name)
					for i in ctype_list:
						if len(i.name) < name_length:
							ctype=i
							name_length=len(ctype.name)
				model_class=ctype.model_class()
				for b in values:
					value=b.strip()
					d=model_class.objects.filter(nombre__startswith=value)
					if len(d) > 0:
						variable_value=d[0]
						if len(d) > 1:
							name_length=len(variable_value.nombre)
							for i in d:
								if len(i.nombre)<name_length:
									variable_value=i
									name_length=len(variable_value.nombre)
						new_query_string+="&"+camelcase(modelname)+"="+str(variable_value.pk)
					else:
						try:
							int(value)
							e=model_class.objects.filter(pk=int(value))
							if len(e) > 0:
								new_query_string+="&"+camelcase(modelname)+"="+str(value)
						except ValueError:
							pass
	new_query_string=new_query_string.lstrip("&")
	return new_query_string

def reverse_translate_query(query):
	new_query_string=u''
	for i in query.lists():
		modelname=get_verbose_name(i[0])
		value=i[1]
		if modelname=='start date':
			modelname='desde'
		if modelname=='end date':
			modelname='hasta'
		if modelname=='desde' or modelname=='hasta' or modelname=='frecuencia':
			new_query_string+="&"+modelname+"="+value[0]
		else:
			ctype_list = ContentType.objects.filter(name=modelname)
			if len(ctype_list) > 0:
				ctype=ctype_list[0]
				model_class=ctype.model_class()
				for b in value:
					d=model_class.objects.filter(pk=b)
					if len(d) > 0:
						new_query_string+="&"+modelname+"="+d[0].nombre
	new_query_string=new_query_string.lstrip("&")
	return new_query_string


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
		last_date=datetime.date(1920,1,1).timetuple()
		first_date=datetime.date.today().timetuple()
		pk_list=[]
		graphs=[]
		mercados = form.cleaned_data['Mercado']
		productos = form.cleaned_data['Producto']
		frecuencias = form.cleaned_data['Frecuencia']
		estaciones_de_lluvia = form.cleaned_data['EstacionDeLluvia']
		start_date = form.cleaned_data['StartDate']
		end_date = form.cleaned_data['EndDate']
		mercado_count=len(mercados)
		producto_count=len(productos)
		lluvia_count=len(estaciones_de_lluvia)
		if mercado_count > 0 and producto_count > 0:
			dollar={'unit':'USD','month':{},'year':{},'day':{}}
			euro={'unit':'Euro','month':{},'year':{},'day':{}}
		pricectype = ContentType.objects.get(app_label__exact='precios', name__exact='prueba')
		lluviactype = ContentType.objects.get(app_label__exact='lluvia', name__exact='prueba')
		for c in frecuencias:
			if c=='diario':
				frecuencia='day'
			elif c=='mensual':
				frecuencia='month'
			elif c=='anual':
				frecuencia='year'
			else:
				frecuencia=c
			for i in mercados:
				for b in productos:
					graph,dollar,euro,pk_list,first_date,last_date=price_graph(mercado=i,producto=b,frecuencia=frecuencia,start_date=start_date,end_date=end_date,mercado_count=mercado_count,producto_count=producto_count,dollar=dollar,euro=euro,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=pricectype)
					if not graph==None:
						graphs.append(graph)
		for d in estaciones_de_lluvia:
			graph,pk_list,first_date,last_date=lluvia_graph(lluvia=d,start_date=start_date,end_date=end_date,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=lluviactype)
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
				
		headline+=": "+str(datetime.date.fromtimestamp(mktime(first_date)))+"&ndash;"+str(datetime.date.fromtimestamp(mktime(last_date)))
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

def price_graph(mercado,producto,frecuencia,start_date,end_date,mercado_count,producto_count,dollar,euro,pk_list,first_date,last_date,ctype):
	queryset = None
	if frecuencia=='day':
		queryset = PrecioPrueba.objects.filter(producto=producto,mercado=mercado,fecha__range=[start_date,end_date]).values('fecha','pk','maximo','minimo').order_by('fecha')
	else:
		cursor = connection.cursor()
		cursor.execute("select producto_id as producto, mercado_id as mercado, date_trunc('"+frecuencia+"',fecha) as fecha, avg(maximo) as maximo, avg(minimo) as minimo from precios_prueba where producto_id = "+str(producto.pk)+" and mercado_id = "+str(mercado.pk)+" and fecha > '"+start_date.strftime('%Y-%m-%d')+"' and fecha < '"+end_date.strftime('%Y-%m-%d')+"' group by date_trunc('"+frecuencia+"',fecha), producto_id, mercado_id order by fecha;")
		queryset=[]
		for row in cursor.fetchall():
			row_dic={'fecha':row[2],'maximo':row[3],'minimo':row[4],'producto':row[0],'mercado':row[1]}
			queryset.append(row_dic)
#		queryset =PrecioPrueba.objects.filter(producto=producto,mercado=mercado,fecha__range=[start_date,end_date]).extra(select={'fecha': "date_trunc('"+frecuencia+"', fecha)"}).values('fecha','producto','mercado','maximo','minimo').annotate(maximo=Avg('maximo'),minimo=Avg('minimo')).order_by('fecha')
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
		fecha=mktime(i['fecha'].timetuple())/1000
		adjusted_fecha=fecha
		if frecuencia=='day':
			adjusted_fecha+=22
		elif frecuencia=='month':
			adjusted_fecha+=1365
		elif frecuencia=='year':
			adjusted_fecha+=15800
		precio=int(i['maximo'])		
		if i['maximo'] != i['minimo']:
			min_data_dic[int(adjusted_fecha)]=int(i['minimo'])
		if not str(int(adjusted_fecha)) in dollar[frecuencia]:
			if frecuencia=='day':
				dollar[frecuencia][str(int(adjusted_fecha))]=float(USD.objects.get(fecha__exact=i['fecha']).cordobas)
				euro[frecuencia][str(int(adjusted_fecha))]=float(Euro.objects.get(fecha__exact=i['fecha']).cordobas)
			else:
				cursor = connection.cursor()
				cursor.execute("select avg(cordobas) from valuta_usd where date_trunc('month',fecha)='"+i['fecha'].strftime('%Y-%m-%d')+"';")
				dollar[frecuencia][str(int(adjusted_fecha))]= float(cursor.fetchone()[0])
				cursor.execute("select avg(cordobas) from valuta_euro where date_trunc('month',fecha)='"+i['fecha'].strftime('%Y-%m-%d')+"';")
				euro[frecuencia][str(int(adjusted_fecha))]= float(cursor.fetchone()[0])				
#				dollar[frecuencia][str(int(adjusted_fecha))]=float(USD.objects.filter(fecha__exact=i['fecha']).extra(select={'fecha': "date_trunc('"+frecuencia+"', fecha)"}).values('fecha').annotate(cordobas=Avg('cordobas'))[0]['cordobas'])
#				euro[frecuencia][str(int(adjusted_fecha))]=float(Euro.objects.filter(fecha__exact=i['fecha']).extra(select={'fecha': "date_trunc('"+frecuencia+"', fecha)"}).values('fecha').annotate(cordobas=Avg('cordobas'))[0]['cordobas'])
		adjusted_fecha=int(adjusted_fecha)
		if frecuencia=='day':
			unique_pk=str(content_type)+"_"+str(i['pk'])		
			list_of_pk.append(str(i['pk']))
			max_data.append([adjusted_fecha,precio,unique_pk])
		else:
			max_data.append([adjusted_fecha,precio])
	if frecuencia=='day':
		pk_list.append([content_type,list_of_pk])
	result={'producto':producto.nombre,'mercado':mercado.nombre,'unit':'cordoba','tipo':'precio','frecuencia':frecuencia}
	if len(min_data_dic)==0:
		result['data']=max_data
	else:
		result['max_data']=max_data
		result['min_data_dic']=min_data_dic
	return result,dollar,euro,pk_list,first_date,last_date

def lluvia_graph(lluvia,start_date,end_date,pk_list,first_date,last_date,ctype):
	queryset =LLuviaPrueba.objects.filter(estacion=lluvia).filter(fecha__range=[start_date,end_date]).order_by('fecha')
	content_type=ctype.id
	if len(queryset)==0:
		return None,pk_list,first_date,last_date
	data=[]
	list_of_pk=[]
	for i in queryset:
		if i.fecha.timetuple() < first_date:
			first_date=i.fecha.timetuple()
		if i.fecha.timetuple() > last_date:
			last_date=i.fecha.timetuple()
		value=str(i.milimetros_de_lluvia)
		fecha=mktime(i.fecha.timetuple())/1000
		fecha=int(fecha)
		unique_pk=str(content_type)+"_"+str(i.pk)		
		list_of_pk.append(str(i.pk))
		data.append([fecha,value,unique_pk])
	pk_list.append([content_type,list_of_pk])
	result={'lluvia':lluvia.nombre,'data':data,'unit':'mm','tipo':'lluvia'}
	return result,pk_list,first_date,last_date

