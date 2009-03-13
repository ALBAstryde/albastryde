# -*- coding: utf-8 -*-

"""
Nicaragua-specific Form helpers
"""

from django.forms import ValidationError
from django.forms.fields import  RegexField, ChoiceField, EMPTY_VALUES
from django.forms.util import smart_unicode
from django.utils.translation import ugettext_lazy as _
import re


class NIPhoneNumberField(RegexField):
    """
    Nicaraguan phone number field. 
    NOTE: Nicaragua will add another digit from April 1st 2009.
    """
    default_error_messages = {
        'invalid': u'Phone numbers must be in the format  XXX-XXXX or XXXXXXX.',
    }

    def __init__(self, *args, **kwargs):
        super(NIPhoneNumberField, self).__init__(r'^\d{3}-\d{4}|^\d{7}$',
                max_length = None, min_length = None, *args, **kwargs)

    def clean(self, value):
        """
        Validates the input and returns a string with only numbers.
        Returns an empty string for empty values
        """
        v = super(NIPhoneNumberField, self).clean(value)
        return v.replace('-', '')

DEPARTAMENT_CHOICES = ( 
    ('BO', _(u'Boaco')), 
    ('CZ', _(u'Carazo')), 
    ('CH', _(u'Chinandega')), 
    ('CT', _(u'Chontales')), 
    ('ES', _(u'Estelí')), 
    ('GR', _(u'Granada')), 
    ('JI', _(u'Jinotega')), 
    ('LE', _(u'León')), 
    ('MZ', _(u'Madriz')), 
    ('M', _(u'Managua')), 
    ('MY', _(u'Masaya')), 
    ('MT', _(u'Matagalpa')), 
    ('NS', _(u'Nueva Segovia')), 
    ('RI', _(u'Rivas')), 
    ('RS', _(u'Río San Juan')), 
    ('RAAN', _(u'Región Autónoma del Atlántico Norte(RAAN)')), 
    ('RAAS', _(u'Región Autónoma del Atlántico Sur(RAAS)')), 
)

    
class NIDepartamentSelect(ChoiceField):
    """
    A Select widget that uses a list of Nicaraguan departaments.
    """
    def __init__(self):
        super(NIDepartamentSelect, self).__init__(choices=DEPARTAMENT_CHOICES)

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

