from django.contrib.contenttypes.models import ContentType
from django.db.models.options import get_verbose_name

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
		if modelname==u'desde' or modelname==u'hasta' or modelname==u'frecuencia':
			new_query_string+="&"+camelcase(modelname)+"="+values[0]
		elif modelname[0:7]==u'incluir':
			new_query_string+="&"+camelcase(modelname)+"=on"
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
		if modelname=='desde' or modelname=='hasta' or modelname=='frecuencia':
			new_query_string+="&"+modelname+"="+value[0]
		elif modelname[0:7]=='incluir':
			new_query_string+="&"+modelname
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
