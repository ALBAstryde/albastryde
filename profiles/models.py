from django.db import models
from django.contrib.auth.models import User
from albastryde.nicalocals import NIPhoneNumberField
from django.db.models.fields import Field
from django.conf import settings
#from alabstryde.lugar import Municipio

class PhoneNumberField(Field):
	def get_internal_type(self):
	       	return "PhoneNumberField"

	def db_type(self):
            	return 'varchar(20)'

	def formfield(self, **kwargs):
      		defaults = {'form_class': NIPhoneNumberField}
       		defaults.update(kwargs)
       		return super(PhoneNumberField, self).formfield(**defaults)


class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	telefono = PhoneNumberField()

        def __unicode__(self):
                if self.user.first_name and self.user.last_name:
                        return self.user.first_name+" "+self.user.last_name
                else:   
                        return self.user.username


	def get_absolute_url(self):
        	return ('profiles_profile_detail', (), { 'username': self.user.username })
	get_absolute_url = models.permalink(get_absolute_url)

