from datetime import date
from time import mktime
from cosecha.models import Cosecha
#from django.db import connection

# Esta es para traducir las fechas de los tiempos
def traducir_fecha(date):
	cosecha_tiempo={}
	if date.month < 3:
		cosecha_tiempo['ano']=date.year-1
		cosecha_tiempo['tiempo']=3
	elif date.month > 2 and date.month < 6:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=1
	elif date.month > 5 and date.month < 9:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=2
	elif date.month > 8:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=3
	return cosecha_tiempo

def traducir_tiempo(ano,tiempo):
	if tiempo==1:
		return date(year=ano,month=3,day=1)
	elif tiempo==2:
		return date(year=ano,month=6,day=1)
	elif tiempo==3:
		return date(year=ano,month=9,day=1)
	return None
	
def cosecha_graph(variable,producto,municipio,start_date,end_date,pk_list,ctype):
	cosecha_start=traducir_fecha(start_date)
	cosecha_end=traducir_fecha(end_date)
	a= Cosecha.objects.filter(ano=cosecha_start['ano']).filter(tiempo__gt= cosecha_start['tiempo']-1)
	b= Cosecha.objects.filter(ano__gt=cosecha_start['ano']).filter(ano__lt=cosecha_end['ano'])
	c= Cosecha.objects.filter(ano=cosecha_end['ano']).filter(tiempo__lt=cosecha_end['tiempo']+1)
	d= a | b| c
	queryset=d.filter(producto=producto).filter(municipio=municipio)
	content_type=ctype.id
	if len(queryset)==0:
		return None,pk_list
	data=[]
	list_of_pk=[]
	for i in queryset:
		fecha=traducir_tiempo(ano=i.ano,tiempo=i.tiempo)
		if variable=='area estimada':
                         value=i.area_estimada
                         unit= 'mz'
                 elif variable=='producto estimado':
                         value=i.producto_estimado
                         unit='lb/mz'
                 elif variable=='area sembrada':
                         value=i.area_sembrada
                         unit='mz'
                 elif variable=='area cosechada':
                         value=i.area_cosechada
                         unit='mz'
                 elif variable=='producto obtenido':
                         value=i.producto_obtenido
                         unit='lb/mz'
                 elif variable=='rendimiento estimado':
                         value=i.rendimiento_estimado()
                         unit='lb/mz'
		else:
			value=0
			unit=""
		fecha_numero=mktime(fecha.timetuple())
		fecha_numero=int(fecha_numero)
		unique_pk=str(content_type)+"_"+str(i.pk)
		list_of_pk.append(str(i.pk))
		data.append([fecha_numero,value,unique_pk])
	pk_list.append([content_type,list_of_pk])
	result = {'included_variables':{'municipio':municipio.nombre, 'cosecha_producto':producto.nombre, 'tipovariable':variable},'data':data,'source':'raw','unit':unit,'type':'cosecha '+variable,'frequency':'monthly','main_variable_js':'"'+variable+' de "+this.included_variables.cosecha_producto','place_js':'this.included_variables.municipio','normalize_factor_js':'this.start_value','display':'bars'}
	return result,pk_list

