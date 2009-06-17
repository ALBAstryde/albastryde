from valuta.models import USD,Euro
from django.db.models import Max
import datetime
from valuta.pyQ import getTickers


def get_Euros():
	previous_data=True
	try:
		first_date=Euro.objects.aggregate(Max('fecha'))['fecha__max'].strftime('%Y%m%d')
	except:
		first_date='19900101'
		previous_data=False
	last_date=datetime.date.today().strftime('%Y%m%d')
	if not first_date==last_date:
		valuta_list=getTickers(first_date,last_date,["NIOEUR=X"])
		for i in valuta_list:	
			fecha=datetime.datetime.strptime(i[1],'%Y%m%d')
			if i[1]==first_date and previous_data:
				new_Euro_entry=Euro.objects.get(fecha=fecha)
				new_Euro_entry.cordobas=i[2]
			else:
				new_Euro_entry=Euro(fecha=fecha,cordobas=i[2])	
			new_Euro_entry.save()
	return True

def get_USD():
	previous_data=True
	try:
		first_date=USD.objects.aggregate(Max('fecha'))['fecha__max'].strftime('%Y%m%d')
	except:
		first_date='19900101'
		previous_data=False
	last_date=datetime.date.today().strftime('%Y%m%d')
	if not first_date==last_date:
		valuta_list=getTickers(first_date,last_date,["NIOUSD=X"])
		for i in valuta_list:
			fecha=datetime.datetime.strptime(i[1],'%Y%m%d')
			if i[1]==first_date and previous_data:
				new_USD_entry=USD.objects.get(fecha=fecha)
				new_USD_entry.cordobas=i[2]
			else:
				new_USD_entry=USD(fecha=fecha,cordobas=i[2])	
			new_USD_entry.save()
	return True

