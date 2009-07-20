# -*- coding: utf-8 -*-
from precios.builder import precio_graph, precio_builder
from lluvia.builder import lluvia_graph, lluvia_builder
from cosecha.builder import cosecha_graph, cosecha_builder
from semilla.builder import semilla_graph, semilla_builder

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
		frecuencias = form.cleaned_data['Frecuencia']
		frequencies=[]

		for frecuencia in frecuencias:
			frequencies.append(eng_dic[frecuencia])

# MUY IMPORTANTE. AQUI ESTAN 4 LINEAS PARA CADA UNO DE LOS TIPOS DE GRAFICOS!!!

		precio_graphs,precio_pk_list,dollar,euro=precio_builder(form_data=form.cleaned_data,frequencies=frequencies)
		if not precio_graphs == None:
			graphs+=precio_graphs
			pk_list+=precio_pk_list

		cosecha_graphs,cosecha_pk_list=cosecha_builder(form_data=form.cleaned_data,frequencies=frequencies)
		if not cosecha_graphs == None:
			graphs+=cosecha_graphs
			pk_list+=cosecha_pk_list
		
		semilla_graphs,semilla_pk_list=semilla_builder(form_data=form.cleaned_data,frequencies=frequencies)
		if not semilla_graphs == None:
			graphs+=semilla_graphs
			pk_list+=semilla_pk_list
		
		lluvia_graphs,lluvia_pk_list=lluvia_builder(form_data=form.cleaned_data,frequencies=frequencies)
		if not lluvia_graphs == None:
			graphs+=lluvia_graphs
			pk_list+=lluvia_pk_list

		rdict.update({'graphs':graphs})
		if len(precio_graphs) > 0:
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
