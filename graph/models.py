from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class StatisticsFormVariable(models.Model):
	nombre = models.CharField(unique=True,max_length="60")  
   
	def save(self):  
		self.nombre=self.nombre.translate({91: None, 61: None, 38: None, 93: None}).strip() # delete u'[]=&' from string and whitespace from ends 
        	super(StatisticsFormVariable, self).save()  

	def __unicode__(self):
		return self.nombre

	class Meta:
		abstract = True
		ordering = ['nombre']

class Timestamped(models.Model):
	creado_a = models.DateTimeField(editable=False,default=datetime.now)  
	actualizado_a = models.DateTimeField(editable=False,default=datetime.now)  
	creado_por = models.ForeignKey(User, editable=False, blank=True, null=True, related_name="creator")  
	actualizado_por = models.ForeignKey(User, editable=False, blank=True, null=True, related_name="updater")  
   
	def save(self):  
		now = datetime.now()  
		if not self.id:  
			self.creado_a = now 
			self.creado_por=self.actualizado_por
		self.actualizado_a = now  	 
		super(Timestamped, self).save()  

	class Meta:
		abstract = True

class Approvable(Timestamped):  
	es_aprobado = models.BooleanField(verbose_name="aprobado",editable=False,default=False)  
	aprobado_a = models.DateTimeField(blank=True, editable=False, null=True)  

	class Meta:
        	permissions = (("puede_aprobar", "Puede aprobar"),)
		abstract = True
 
	def save(self):  
        	if ((self.actualizado_por) and (self.actualizado_por.has_perm(str(self)+'.puede_aprobar'))):
			if self.es_aprobado==False:
				self.aprobado_a=datetime.now()
	        	 	self.es_aprobado = True
		else:   
                	self.es_aprobado = False
			self.approved_at = None
		super(Approvable, self).save() 
