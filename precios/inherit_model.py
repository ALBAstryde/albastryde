#import types
#from copy import deepcopy
from django.db import models
#from django.db.models.fields import Field
#from django.db.models.base import ModelBase
from django.contrib.auth.models import User
from datetime import datetime


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
     es_aprobado = models.BooleanField(verbose_name="aprobado",editable=False,
         default=False)  
     aprobado_a = models.DateTimeField(blank=True, editable=False, null=True)  

     class Meta:
         permissions = (("puede_aprobar", "Puede aprobar"),)
	 abstract = True
 
     def save(self):  
         if (self.actualizado_por.has_perm(str(self)+'.puede_aprobar')):
#         if (self.has_perm('puede_aprobar',self.actualizado_por)):
		if self.es_aprobado==False:
			self.aprobado_a=datetime.now()
	         	self.es_aprobado = True
         else:   
                self.es_aprobado = False
		self.approved_at = None
         super(Approvable, self).save()  


  
#     def __setattr__(self, name, value):  
          #ignore the first calls when Field instances are still being  
          #replaced by their plain values.  
#         if not isinstance(self.is_approved, models.Field):  
             # if we are set to "approved", remember to update the timestamp  
#             if name == 'is_approved' and value != self.is_approved and value:  
#                 self._date_needs_update = True  
#         return super(Approvable, self).__setattr__(name, value)  
   
#     def save(self):  
#         if self.is_approved:  
#             # for new items, always update  
#             if (not self.id): update_approved_date = True  
#             # for existing items, check if the value changed  
#             else:  
#                 update_approved_date = getattr(self, '_date_needs_update', False)  
#                 self._date_needs_update = False  
#   
#             if update_approved_date:  
#                 self.approved_at = datetime.now()  
#   
#         super(Approvable, self).save()  

