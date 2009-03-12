from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from precios.models import Prueba
from django.utils import simplejson
from graph.forms import DbForm
from coffin.shortcuts import render_to_response
from valuta.models import USD,Euro
from wiki.views import menu_list
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment


import operator
import itertools
import pprint
import datetime
from time import mktime


def get_js_graph(request,query_set=None,javascript=False,model=None):
#	cl=query
#        if request.method == "POST" and request.is_ajax():
#                json = simplejson.dumps(rdict, ensure_ascii=False)
#                return HttpResponse( json, mimetype='application/javascript')
        if request.method == "POST":# and request.is_ajax():
#	elif request.method == "POST":
		form = DbForm(request.POST)
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
			last_date=datetime.date(1970,1,1)
			first_date=datetime.date.today()
			dollar={'unit':'USD'}
			euro={'unit':'Euro'}			
			pk_list=[]
			graphs=[]
			mercados = form.cleaned_data['mercado']
			productos = form.cleaned_data['producto']
			start_date = form.cleaned_data['start_date']
			end_date = form.cleaned_data['end_date']
			mercado_count=len(mercados)
			producto_count=len(productos)
#			valuta_count=1
#			global last_date, first_date
		        pricectype = ContentType.objects.get(app_label__exact='precios', name__exact='prueba')
			for i in mercados:
				for b in productos:
					graph,dollar,euro,pk_list,first_date,last_date=price_graph(mercado=i,producto=b,start_date=start_date,end_date=end_date,mercado_count=mercado_count,producto_count=producto_count,dollar=dollar,euro=euro,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=pricectype)
					if not graph==None:
						graphs.append(graph)
			rdict.update({'graphs':graphs})
			rdict.update({'dollar':dollar})
			rdict.update({'euro':euro})

			mercado_name=""
			for i in mercados:
				mercado_name+=i.nombre+", "
			mercado_name=mercado_name.strip(", ")
			if len(mercado_name)>60:
				mercado_name="el mercado"
			producto_name=""
			for i in productos:
				producto_name+=i.nombre+", "
			producto_name=producto_name.strip(", ")
			if len(producto_name)>60:
				producto_name="Unos productos"

			headline=producto_name.capitalize()+" en "+mercado_name+ ": "+str(first_date)+"&ndash;"+str(last_date)
			rdict.update({'headline':headline})
			comments={}
			for content_type in pk_list :
	                	all_comments_qs=Comment.objects.filter(content_type=content_type[0], object_pk__in=content_type[1],is_removed=False)
				if (request.user.has_perm('comments.can_manage')):
					comments_qs = all_comments_qs
				elif (request.user.is_authenticated()):
					my_comments_qs=all_comments_qs.filter(user=request.user)
					public_comments_qs=all_comments_qs.filter(is_public=True)	
					comments_qs= my_comments_qs | public_comments_qs
				else:
					comments_qs=all_comments_qs.filter(is_public=True)	
				if len(comments_qs)>0:
					for i in comments_qs:
						unique_pk=str(content_type[0])+"_"+str(i.object_pk)
						if not unique_pk in comments:
							comments[unique_pk]={}
						if (request.user.has_perm('comments.can_manage') or (i.user==request.user and request.user.has_perm('comments.change_comment'))):
							puede_editar=True
						else:
							puede_editar=False
						comments[unique_pk][i.pk]=[i.comment,i.name,puede_editar,i.is_public]
					rdict.update({'comments':comments})
	        json = simplejson.dumps(rdict, ensure_ascii=False)
        	return HttpResponse( json, mimetype='application/javascript')
	else:
		username=""
		if request.user.is_anonymous()==True:
			username = "Anonymous"
		else:
			username = request.user.get_full_name()
			if username=="":
				username = request.user.username
		form =DbForm()
		return render_to_response("/get_graph.html", {"form":form,"request":request,"menu_list":menu_list,"username":username})	


def price_graph(mercado,producto,start_date,end_date,mercado_count,producto_count,dollar,euro,pk_list,first_date,last_date,ctype):
	queryset =Prueba.objects.filter(producto=producto).filter(mercado=mercado).filter(fecha__range=[start_date,end_date]).order_by('fecha')
	content_type=ctype.id
	if len(queryset)==0:
		return None,dollar,euro,pk_list,first_date,last_date
	data=[]
	list_of_pk=[]
	for i in queryset:
		if i.fecha < first_date:
			first_date=i.fecha
		if i.fecha > last_date:
			last_date=i.fecha
		if i.maximo != i.minimo:
			precio=int((i.maximo+i.minimo)/2)
		else:
			precio=int(i.maximo)
		fecha=mktime(i.fecha.timetuple())*1000#+1e-6*fecha.microsecond)
		if not str(int(fecha)) in dollar:
			dollar[str(int(fecha))]=float(USD.objects.get(fecha__exact=i.fecha).cordobas)
			euro[str(int(fecha))]=float(Euro.objects.get(fecha__exact=i.fecha).cordobas)
		fecha=int(fecha)
		unique_pk=str(content_type)+"_"+str(i.pk)		
		list_of_pk.append(str(i.pk))
		data.append([fecha,precio,unique_pk])
	pk_list.append([content_type,list_of_pk])
	label=""
	if producto_count>1:
		label+=producto.nombre+" "
	if mercado_count>1:
		label+="en "+mercado.nombre+" "
	#if valuta_count>1:
	#	label+="(cordobas)"+" "
	label=label.strip()
	if label=="":
		label==producto.nombre
	
	result={'label':label,'data':data,'unit':'cordoba'}
	return result,dollar,euro,pk_list,first_date,last_date



def get_graph(query_set=None,model=None):
#	cl=query
	if query_set and model:
#		output=str(request)
		if model==Prueba:
			#output="Price graph"
	                #output+=str(query_set)
			dic_list = [] #list of all items returned by query
			mercados_usados=[]#all the markets data comes from
			productos_usados=[]# all the products present in the first date
			for i in query_set:
				if i.maximo != i.minimo:
					precio=(i.maximo+i.minimo)/2
				else:
					precio=i.maximo
				if not i.mercado in mercados_usados:
					mercados_usados.append(i.mercado)
				fecha=i.fecha
				Javascript_timestamp=mktime(fecha.timetuple())*1000#+1e-6*fecha.microsecond
				item={'producto':i.producto,'fecha':Javascript_timestamp,'precio':precio}
				dic_list.append(item)
			dic_list.sort(key=operator.itemgetter('fecha'))
			list1 = []
			for key, items in itertools.groupby(dic_list, operator.itemgetter('fecha')):
				list1.append(list(items))
			#if (len(mercados_usados)>1):#date is from more than one market, so we need to find average prices for every product first				
			if 1:
				list2=[]
				for date_group in list1:
					new_list=[]
					date_group.sort(key=operator.itemgetter('producto'))
					for key, items in itertools.groupby(date_group, operator.itemgetter('producto')):
						new_list.append(list(items))
					#another_new_list=[]
					new_dic={}
					new_dic['fecha']=date_group[0]['fecha']
					for product_group in new_list:
						producto=product_group[0]['producto']
						#fecha=product_group[0]['fecha']
						size=len(product_group)
						sum=0
						for k in range(size):
							sum += int((product_group[k]['precio']))
						average = sum/float(size)
						#item={'producto':producto,'fecha':fecha,'precio':average}
						#another_new_list.append(item)
						new_dic[producto]=average
					#list2.append(another_new_list)
					list2.append(new_dic)
#			else:
#				list2=list1
			last_known_prices=list2[0].copy()
			del last_known_prices['fecha']
			first_known_prices=last_known_prices.copy()
			initial_price_index=0
#			for producto, precio in last_known_prices.items():
#				initial_price_index+=precio
			list3=[]
			for date_group in list2:
				fecha=date_group['fecha']
				sum=0
				for producto, precio in last_known_prices.items():
					if date_group.has_key(producto):
						sum=sum+(date_group[producto]/first_known_prices[producto])
						last_known_prices[producto]=date_group[producto]
					else:
						sum+=(precio/first_known_prices[producto])
				price_index=sum/len(first_known_prices.items())
				list3.append([fecha,price_index])
			output=str(list3)

				#if not item['producto'] in productos_usados:					
				#	productos_usados.append(item['producto'])

				
						

#                output+=str(cl.opts)
#                output+=str(cl.lookup_opts)
#                output+=str(cl.list_display)
#                output+=str(cl.list_display_links)

#                output+=str(cl.list_filter)

#                output+=str(cl.date_hierarchy)                                                      
#                output+=str(cl.search_fields)
#                output+=str(cl.list_select_related)
#                output+=str(cl.list_per_page)
#                output+=str(cl.model_admin)
#                output+=str(cl.page_num)
#                output+=str(cl.show_all)
#                output+=str(cl.is_popup)
#                output+=str(cl.to_field)
#                output+=str(cl.params)
#                output+=str(cl.order_field)
#                output+=str(cl.query)
#                output+=str(cl.query_set)
#                output+=str(cl.get_results)
#                output+=str(cl.get_query_string)
#                output+=str(cl.title)
#                output+=str(cl.filter_specs)
#                output+=str(cl.get_filters)
#                output+=str(cl.pk_attname) 
		return output
	else:
		return ""
















def dget_graph(request=None,query=None,tipo='precios'):
        if 1:
#        if cl.method == "POST":
#        if cl.method == "POST" and cl.is_ajax():
		if "producto__id__exact" in query:
			if "mercado__id_exact" in query:
				numeros=one_producto_one_mercado(query)
			else:			
				numeros=one_producto_all_mercados(query)
		else:
			if "mercado__id_exact" in query:
				numeros=all_productos_one_mercado(query)
			else:			
				numeros=all_products_all_mercados(query)
		rdict={'quatsch':numeros}
#                json = simplejson.dumps(rdict, ensure_ascii=False)
#                return HttpResponse( json, mimetype='application/javascript')

def one_producto_one_mercado (query):
	producto=which_producto(query)
	mercado=which_mercado(query)
	dates=date_range(query)
	return producto+mercado+dates

def one_producto_all_mercados (query):
	producto=which_producto(query)
	dates=date_range(query)
	return producto+dates

def all_productos_one_mercado (query):
	mercado=which_mercado(query)
	dates=date_range(query)
	return mercado+dates

def all_productos_all_mercados (query):
	dates=date_range(query)
	return dates

def which_producto(query):
	productstart = query.find("producto__id__exact=")
	if not productstart==-1:
		productstart=productstart+19
		productend = query.find("&",productstart)
#		if productend==-1:
			
	
	return productstart

def which_mercado(query):
	start = query.find("mercado__id__exact=")
	return start		


def date_range(query):
	year = query.find("fecha__year=")
	if year== -1:
		return 0
	else:
		month = query.find("fecha__month=")
		if month== -1:
			return year
		else:
			day = query.find("fecha__day=")
			if day==-1:
				return year+month
			else:
				return year+month+day
