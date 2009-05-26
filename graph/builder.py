from precios.builder import precio_graph
from lluvia.builder import lluvia_graph
from cosecha.builder import cosecha_graph

from graph.forms import DbForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from datetime import date
from time import mktime

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
		pk_list=[]
		graphs=[]
		municipio_queryset = form.cleaned_data['Municipio']
		municipios=[]
		for municipio in municipio_queryset:
			municipios.append(municipio)
		departamentos = form.cleaned_data['Departamento']
		mercados_queryset = form.cleaned_data['Mercado']
		mercados=[]
		for mercado in mercados_queryset:
			mercados.append(mercado)
		productos = form.cleaned_data['Producto']
		frecuencias = form.cleaned_data['Frecuencia']
		estaciones_de_lluvia_queryset = form.cleaned_data['EstacionDeLluvia']
		estaciones_de_lluvia=[]
		for estacion in estaciones_de_lluvia_queryset:
			estaciones_de_lluvia.append(estacion)
		frequencies=[]
		for frecuencia in frecuencias:
			frequencies.append(eng_dic[frecuencia])
		include_lluvia = form.cleaned_data['IncluirLluvia']
		cosecha_variable = form.cleaned_data['CosechaVariable'] #este es para cosecha
		cosecha_producto = form.cleaned_data['CosechaProducto']
		start_date = form.cleaned_data['Desde']
		end_date = form.cleaned_data['Hasta']
		for departamento in departamentos:
			for municipio in departamento.municipios.iterator():
				municipios.append(municipio)

		if len(productos) > 0:		
			for municipio in municipios:
				for mercado in municipio.mercado_set.all().iterator():
					mercados.append(mercado)
		if include_lluvia:
			for municipio in municipios:
				for estacion in municipio.estaciondelluvia_set.all().iterator():
					estaciones_de_lluvia.append(estacion)

		if len(mercados) > 0 and len(productos) > 0:
			dollar={'unit':'USD','monthly':{},'annualy':{},'daily':{}}
			euro={'unit':'Euro','monthly':{},'annualy':{},'daily':{}}
		pricectype = ContentType.objects.get(app_label__exact='precios', name__exact='prueba')
		lluviactype = ContentType.objects.get(app_label__exact='lluvia', name__exact='prueba')
		cosechactype = ContentType.objects.get(app_label__exact='cosecha', name__exact='cosecha')

		# Aqui se llaman las funciones para hacer cada uno de los graficos

		for frequency in frequencies:
			for i in mercados:
				for b in productos:
					graph,dollar,euro,pk_list=precio_graph(mercado=i,producto=b,frequency=frequency,start_date=start_date,end_date=end_date,dollar=dollar,euro=euro,pk_list=pk_list,ctype=pricectype)
					if not graph==None:
						graphs.append(graph)
			for d in estaciones_de_lluvia:
				graph,pk_list=lluvia_graph(estacion=d,frequency=frequency,start_date=start_date,end_date=end_date,pk_list=pk_list,ctype=lluviactype)
				if not graph==None:
					graphs.append(graph)
			for d in cosecha_variable:
				for e in municipios:
					for i in cosecha_producto:
						graph,pk_list=cosecha_graph(variable=d,municipio=e,producto=i,start_date=start_date,end_date=end_date,pk_list=pk_list,ctype=cosechactype)
						if not graph==None:
							graphs.append(graph)	



		rdict.update({'graphs':graphs})
		if len(mercados) > 0 and len(productos) > 0:
			rdict.update({'dollar':dollar})
			rdict.update({'euro':euro})

		# Lo siguiente es para hacer los comentarios

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
