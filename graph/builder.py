from precios.models import Prueba as PrecioPrueba
from lluvia.models import Prueba as LLuviaPrueba
from graph.forms import DbForm
from valuta.models import USD,Euro
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment

import operator
import itertools
import pprint
import datetime
from time import mktime
from django.http import QueryDict

def translate_query_string(query_string):
	word_query=QueryDict(query_string)
	new_query_string=u''
	for i in word_query.lists():
		model= i[0]
		value=i[1]
		if model=='desde':
			model='start_date'
		if model=='hasta':
			model='end_date'
		if model=='start_date' or model=='end_date':
			new_query_string+="&"+model+"="+value[0]
		else:
			ctype_list = ContentType.objects.filter(name=model)
			if len(ctype_list) > 0:
				ctype=ctype_list[0]
				model_class=ctype.model_class()
				for b in value:
					d=model_class.objects.filter(nombre=b)
					if len(d) > 0:
						new_query_string+="&"+model+"="+str(d[0].pk)
	new_query_string=new_query_string.lstrip("&")
	return new_query_string

def reverse_translate_query(query):
	new_query_string=u''
	for i in query.lists():
		model=i[0]
		value=i[1]
		if model=='start_date':
			model='desde'
		if model=='end_date':
			model='hasta'
		if model=='desde' or model=='hasta':
			new_query_string+="&"+model+"="+value[0]
		else:
			ctype_list = ContentType.objects.filter(name=model)
			if len(ctype_list) > 0:
				ctype=ctype_list[0]
				model_class=ctype.model_class()
				for b in value:
					d=model_class.objects.filter(pk=b)
					if len(d) > 0:
						new_query_string+="&"+model+"="+d[0].nombre
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
		last_date=datetime.date(1920,1,1)
		first_date=datetime.date.today()
		pk_list=[]
		graphs=[]
		mercados = form.cleaned_data['mercado']
		productos = form.cleaned_data['producto']
		lluvias = form.cleaned_data['lluvia']
		start_date = form.cleaned_data['start_date']
		end_date = form.cleaned_data['end_date']
		mercado_count=len(mercados)
		producto_count=len(productos)
		lluvia_count=len(lluvias)
		if mercado_count > 0 and producto_count > 0:
			dollar={'unit':'USD'}
			euro={'unit':'Euro'}			
		pricectype = ContentType.objects.get(app_label__exact='precios', name__exact='prueba')
		lluviactype = ContentType.objects.get(app_label__exact='lluvia', name__exact='prueba')
		for i in mercados:
			for b in productos:
				graph,dollar,euro,pk_list,first_date,last_date=price_graph(mercado=i,producto=b,start_date=start_date,end_date=end_date,mercado_count=mercado_count,producto_count=producto_count,dollar=dollar,euro=euro,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=pricectype)
				if not graph==None:
					graphs.append(graph)
		for c in lluvias:
			graph,pk_list,first_date,last_date=lluvia_graph(lluvia=c,start_date=start_date,end_date=end_date,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=lluviactype)
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
			for i in lluvias:
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
				
		headline+=": "+str(first_date)+"&ndash;"+str(last_date)
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


def price_graph(mercado,producto,start_date,end_date,mercado_count,producto_count,dollar,euro,pk_list,first_date,last_date,ctype):
	queryset =PrecioPrueba.objects.filter(producto=producto).filter(mercado=mercado).filter(fecha__range=[start_date,end_date]).order_by('fecha')
	content_type=ctype.id
	if len(queryset)==0:
		return None,dollar,euro,pk_list,first_date,last_date
	max_data=[]
	min_data_dic={}
	list_of_pk=[]
	for i in queryset:
		if i.fecha < first_date:
			first_date=i.fecha
		if i.fecha > last_date:
			last_date=i.fecha
		fecha=mktime(i.fecha.timetuple())/1000
		precio=int(i.maximo)		
		if i.maximo != i.minimo:
			min_data_dic[int(fecha)]=int(i.minimo)
		if not str(int(fecha)) in dollar:
			dollar[str(int(fecha))]=float(USD.objects.get(fecha__exact=i.fecha).cordobas)
			euro[str(int(fecha))]=float(Euro.objects.get(fecha__exact=i.fecha).cordobas)
		fecha=int(fecha)
		unique_pk=str(content_type)+"_"+str(i.pk)		
		list_of_pk.append(str(i.pk))
		max_data.append([fecha,precio,unique_pk])
	pk_list.append([content_type,list_of_pk])
	result={'producto':producto.nombre,'mercado':mercado.nombre,'unit':'cordoba','tipo':'precio'}
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
		if i.fecha < first_date:
			first_date=i.fecha
		if i.fecha > last_date:
			last_date=i.fecha
		value=str(i.milimetros_de_lluvia)
		fecha=mktime(i.fecha.timetuple())/1000
		fecha=int(fecha)
		unique_pk=str(content_type)+"_"+str(i.pk)		
		list_of_pk.append(str(i.pk))
		data.append([fecha,value,unique_pk])
	pk_list.append([content_type,list_of_pk])
	result={'lluvia':lluvia.nombre,'data':data,'unit':'mm','tipo':'lluvia'}
	return result,pk_list,first_date,last_date

