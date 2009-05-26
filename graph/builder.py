from precios.builder import precio_graph
from lluvia.builder import lluvia_graph
from cosecha.builder import cosecha_graph

#from precios.models import Mercado
#from lluvia.models import Prueba as LLuviaPrueba
from graph.forms import DbForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from datetime import date
from time import mktime
#from cosecha.models import Cosecha

eng_dic={'diario':'daily','mensual':'monthly','anual':'annualy'}

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
		frecuencias = form.cleaned_data['Frecuencia']
		estaciones_de_lluvia_queryset = form.cleaned_data['EstacionDeLluvia']
		estaciones_de_lluvia=[]
		for i in estaciones_de_lluvia_queryset:
			estaciones_de_lluvia.append(i)
		frequencies=[]
		for i in frecuencias:
			frequencies.append(eng_dic[i])
		include_lluvia = form.cleaned_data['IncluirLluvia']
		cosecha_variable = form.cleaned_data['CosechaVariable'] #este es para cosecha
		cosecha_producto = form.cleaned_data['CosechaProducto']
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
		cosechactype = ContentType.objects.get(app_label__exact='cosecha', name__exact='cosecha')
		for frequency in frequencies:
			for i in mercados:
				for b in productos:
					graph,dollar,euro,pk_list,first_date,last_date=precio_graph(mercado=i,producto=b,frequency=frequency,start_date=start_date,end_date=end_date,mercado_count=mercado_count,producto_count=producto_count,dollar=dollar,euro=euro,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=pricectype)
					if not graph==None:
						graphs.append(graph)
			for d in estaciones_de_lluvia:
				graph,pk_list,first_date,last_date=lluvia_graph(estacion=d,frequency=frequency,start_date=start_date,end_date=end_date,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=lluviactype)
				if not graph==None:
					graphs.append(graph)
			for d in cosecha_variable:
				for e in municipios:
					for i in cosecha_producto:
						graph,pk_list,first_date,last_date=cosecha_graph(variable=d,municipio=e,producto=i,start_date=start_date,end_date=end_date,pk_list=pk_list,first_date=first_date,last_date=last_date,ctype=cosechactype)
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
