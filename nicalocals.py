# -*- coding: utf-8 -*-

"""
Nicaragua-specific Form helpers

all copied from http://code.djangoproject.com/attachment/ticket/10203/Ni-localflavor-3.diff

waiting for official inclusion

"""

from django.forms import ValidationError
from django.forms.fields import  RegexField, Select, EMPTY_VALUES
from django.forms.util import smart_unicode
from django.utils.translation import ugettext_lazy as _
import re


class NIPhoneNumberField(RegexField):
    """
    Nicaraguan phone number field. 
    NOTE: Nicaragua will add another digit from April 1st 2009.
    """
    default_error_messages = {
        'invalid': u'Phone numbers must be in the format  XXXX-XXXX or XXXXXXXX.',
    }

    def __init__(self, *args, **kwargs):
        super(NIPhoneNumberField, self).__init__(r'^[ 0-9\-]+$',
                max_length = None, min_length = None, *args, **kwargs)

    def clean(self, value):
        """
        Validates the input and returns a string with only numbers.
        Returns an empty string for empty values
        """

	if value in EMPTY_VALUES:
	    return u''

        v = super(NIPhoneNumberField, self).clean(value)
        v= v.replace('-', '')
	v = v.replace(' ', '')
	if (len(v) == 8):
	    return v
	raise ValidationError(self.default_error_messages['invalid'])

DEPARTAMENT_CHOICES = ( 
    (50, _(u'Boaco')),  
    (75, _(u'Carazo')),  
    (30, _(u'Chinandega')),  
    (65, _(u'Chontales')),  
    (25, _(u'Estelí')),  
    (70, _(u'Granada')),  
    (10, _(u'Jinotega')),  
    (35, _(u'León')),  
    (20, _(u'Madriz')),  
    (55, _(u'Managua')),  
    (60, _(u'Masaya')),  
    (40, _(u'Matagalpa')),  
    (5, _(u'Nueva Segovia')),  
    (80, _(u'Rivas')),  
    (85, _(u'Río San Juan')),  
    (91, _(u'Región Autónoma del Atlántico Norte(RAAN)')),  
    (93, _(u'Región Autónoma del Atlántico Sur(RAAS)')),
)
    
class NIDepartamentSelect(Select):
    """
    A Select widget that uses a list of Nicaraguan departaments.
    """
    def __init__(self):
        super(NIDepartamentSelect, self).__init__(attrs, choices=DEPARTAMENT_CHOICES)

class NICedulaNumberField(RegexField):
    """
    Cedula number(cedula is the identification document to
    vote and make legal stuff in Nicaragua.
    
    The format is 999-999999-9999A where 9 is a number and A is a letter. 
    """
    default_error_messages = {
        'invalid': _('Enter a valid Cedula number in XXX-XXXXXX-XXXXX format.'),
    }
    
    def __init__(self, *args, **kwargs):
        super(NICedulaNumberField, self).__init__(r'^(\d{3})-(\d{6})-(\d{4}[a-zA-z])$',
                max_length = None, min_length = None, *args, **kwargs)


    def clean(self, value):
        value = super(NICedulaNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        else:
            return value

