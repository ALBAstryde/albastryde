# -*- coding: latin-1 -*-
from datetime import datetime
from datetime import date,timedelta
import settings
import sys
import unicodedata
from matplotlib.dates import date2num,drange
from hashlib import sha224
today = date.today()

class Statisticsplot:

	def __init__(self, formula):
		self.formula=formula
		self.producto = "bananas"
#		self.start_date=datetime.date.today()
#		self.end_date=datetime.date.today()
#		self.primer_ano = 0
#		self.ultimo_ano = 0
		self.anos = 10
		self.lugar = "nicaragua"
		self.nivel = "pais"
		self.standardizedformula = self.standardize_formula()
		self.image_file = str(sha224(self.standardizedformula).hexdigest())+".png"
		self.image_file_location = settings.MEDIA_ROOT + "cache/"+self.image_file
		self.image_file_url = settings.MEDIA_URL + "cache/"+self.image_file


	def deespanolizar(self, spanish_text):
		return unicodedata.normalize('NFKD', unicode(spanish_text)).encode('ascii','ignore')
#		return spanish_text.replace('ñ','n').replace('é','e').replace('á','a').replace('ó','o').replace('í','i').replace('ü','u').replace('Ñ','N').replace('É','E').replace('Á','A').replace('Ó','O').replace('Í','I').replace('Ü','U')

#	def create_png(self):
#		pass
	def create_png(self):
#		pass
		#fake values!!!!:
		import random
		graph_xlist=[]
		graph_ylist=[]
		for i in drange(self.start_date,self.end_date,timedelta(days=301)):
			graph_xlist.append(i)
			graph_ylist.append(random.randint(8000,10000))	
		import os
		os.environ['MPLCONFIGDIR'] = settings.MEDIA_ROOT+"cache/" 
		import matplotlib
		from matplotlib import rcParams
		rcParams['text.usetex']=True
#		rcParams['text.latex.unicode']=True
#from matplotlib.pyplot import figure, axes, plot, xlabel, ylabel, title, grid, savefig, show
		matplotlib.use( 'Agg' )
		import pylab
		pylab.clf()
#		pylab.gca().xaxis.set_major_formatter(pylab.ScalarFormatter(useOffset=False))
#		pylab.gca().xaxis.major.formatter.set_scientific(False)
#		pylab.gca().xaxis.set_major_formatter(ScalarFormatter())
#		yearsFmt = DateFormatter("%y")
#		pylab.gca().xaxis.set_major_formatter(yearsFmt)
		pylab.suptitle(self.producto+" "+self.lugar+" ("+self.start_date.strftime("%d.%m.%Y")+" -- "+self.end_date.strftime("%d.%m.%Y")+")")
		pylab.xlabel(r'\textbf{a{\~n}os}')
		pylab.ylabel("kg")
		pylab.plot_date(graph_xlist,graph_ylist,color="#6D458A",linestyle='-')
		ax = pylab.gca()
#�		ax.ticklabel_format(style='plain', axis='x')
		pylab.savefig(self.image_file_location, dpi=72, format='png')
		pylab.close('all') 
		return 1

	def standardize_formula(self):
		b=self.formula.split(",")
		for c in b:
			d = self.deespanolizar(c).split("=")
			if len(d) == 2:
				variable = d[0].lower().strip().replace(' ','_')
				value = d[1].lower().strip()
				if variable == 'producto' or variable == 'product':
					self.producto = value
				elif variable == 'primer_ano' or variable == 'first_year':
					self.start_date= datetime.strptime(value+"-01-01", "%Y-%m-%d").date()
				elif variable == 'ultimo_ano' or variable == 'last_year':
					self.end_date= datetime.strptime(value+"-12-31", "%Y-%m-%d").date()
				elif variable == 'ultima_fecha' or variable == 'last_date' or variable== 'end_date':
					self.end_date= datetime.strptime(value, "%Y-%m-%d").date()
				elif variable == 'primera_fecha' or variable == 'first_date' or variable== 'start_date':
					self.start_date= datetime.strptime(value, "%Y-%m-%d").date()
				elif variable == 'anos' or variable == 'years':
					self.anos = int(value)
				elif variable == 'departamento' or variable == 'county':
					self.lugar = value
					self.nivel = "departamento"		
		if not hasattr(self, 'start_date'):
			if not hasattr(self, 'end_date'):
				self.start_date = datetime.strptime(str(today.year-self.anos)+"-"+str(today.month)+"-"+str(today.day), "%Y-%m-%d").date()
                        	self.end_date = date.today()

                        	#self.ultimo_ano = today.year
			else:
                                #self.primer_ano = self.ultimo_ano-self.anos
                                self.start_date = datetime.strptime(str(self.end_date.year-self.anos)+"-"+str(self.end_date.month)+"-"+str(self.end_date.day), "%Y-%m-%d").date()
		else:
                        if not hasattr(self, 'end_date'):
				self.end_date=datetime.strptime(str(self.start_date.year+self.anos)+"-"+str(self.start_date.month)+"-"+str(self.start_date.day), "%Y-%m-%d").date()
                                #self.ultimo_ano = self.primer_ano+self.anos
                        else:
				self.anos=self.end_date.year-self.start_date.year#bad calculation!
		if self.end_date > today:
			self.end_date = today
#		if self.primer_ano > self.ultimo_ano :
#			self.primer_ano = self.ultimo_ano - 10
#                if self.start_date > self.end_date :
#                        self.end_date = (str(today.year-10)+"-"+str(today.month)+"-"+str(today.day), "%Y-%m-%d")
#		if self.nivel == 'departamento' ##check if departamento exists
		standardized_formula='producto='+self.producto+',start_date='+self.start_date.strftime("%Y-%m-%d")
		standardized_formula+=',end_date='+self.end_date.strftime("%Y-%m-%d")+',nivel='+self.nivel+',lugar='+self.lugar
		return standardized_formula

def main():
	opts=sys.argv
	hans = Statisticsplot("producto=leche,primer_ano=1994,ultimo_ano=2001,departamento=chinandega")
	peter = hans.standardizedformula
	hans.create_png()
	print peter
if __name__ == "__main__":
	main()

