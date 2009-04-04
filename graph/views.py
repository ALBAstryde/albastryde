from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from graph.forms import DbForm
from coffin.shortcuts import render_to_response
from wiki.views import menu_list
from graph.builder import build_graph,translate_query_string,reverse_translate_query

import operator
import itertools
import pprint
import datetime
from time import mktime
from django.http import QueryDict

def show_form(request,query_set=None,javascript=False,model=None):
        if request.method == "POST" and request.is_ajax():
		query = request.POST
		user = request.user
		rdict = build_graph(query,user)
		query_link=reverse_translate_query(query)
		rdict['query_link']=query_link
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
		form = DbForm()
		return render_to_response("/graph_form.html", {"form":form,"request":request,"menu_list":menu_list,"username":username})	

def show_graph(request,query_string):
	user = request.user
	new_query_string = translate_query_string(query_string)
	query = QueryDict(new_query_string)
	rdict = build_graph(query,user)
	json = simplejson.dumps(rdict, ensure_ascii=False)
	return render_to_response("/graph.html", {"request":request,"json":json,"menu_list":menu_list})	
