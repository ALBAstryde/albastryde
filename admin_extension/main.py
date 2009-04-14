from django import forms
from django import template
from django.db import models
from django.forms.models import BaseInlineFormSet, save_instance
from django.contrib.admin.options import ModelAdmin as BaseModelAdmin
from django.contrib.admin.options import InlineModelAdmin as BaseInlineModelAdmin
from django.shortcuts import render_to_response
from django.utils.text import get_text_list, capfirst
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ValidationError, ErrorList

class AutopopulateModelForm(forms.ModelForm):
    """
    Subclasses ModelForm to add autopopulated fields functionality.
    
    Autopopulated fields are specified in the 'Meta' subclass by the
    'autopopulate' parameter, which is a dictionary that maps field names 
    to callables. The field name specifies the field to filter on, the 
    callable takes (request, instance) and returns the value to match.
    
    The current request object should be passed in to the constructor.
    Alternately it can be set as a class attribute, this is allowed
    to enable use by the ModelAdmin class below.
    """
    def __init__(self, *args, **kwargs):
        if getattr(kwargs, 'request', None) is not None:
            self.request = request
        if getattr(self._meta, 'autopopulate', None) is None:
            self._meta.autopopulate = []
        super(AutopopulateModelForm, self).__init__(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        """Override of ModelForm.save that correctly handles
            autopopulated fields."""
        if self._meta.autopopulate:
            for field, func in self._meta.autopopulate.iteritems():
                setattr(self.instance, field, func(self.request, self.instance))
        return super(AutopopulateModelForm, self).save(*args, **kwargs)
        
    def validate_unique(self):
        """Override of ModelForm.validate_unique that correctly handles
            autopopulated fields."""
        from django.db.models.fields import FieldDoesNotExist

        # Gather a list of checks to perform. Since this is a ModelForm, some
        # fields may have been excluded; we can't perform a unique check on a
        # form that is missing fields involved in that check.
        unique_checks = []
        for check in self.instance._meta.unique_together[:]:
            fields_on_form = [field for field in check if field in self.fields or field in 
self._meta.autopopulate]
            if len(fields_on_form) == len(check):
                unique_checks.append(check)
        
        form_errors = []
    
        # Gather a list of checks for fields declared as unique and add them to
        # the list of checks. Again, skip fields not on the form.
        for name, field in self.fields.items():
            try:
                f = self.instance._meta.get_field_by_name(name)[0]
            except FieldDoesNotExist:
                # This is an extra field that's not on the ModelForm, ignore it
                continue
            # MySQL can't handle ... WHERE pk IS NULL, so make sure we
            # don't generate queries of that form.
            is_null_pk = f.primary_key and self.cleaned_data[name] is None
            if name in self.cleaned_data and f.unique and not is_null_pk:
                unique_checks.append((name,))
            
        # Don't run unique checks on fields that already have an error.
        unique_checks = [check for check in unique_checks if not [x in self._errors for x in check if 
x in self._errors]]
    
        for unique_check in unique_checks:
            # Try to look up an existing object with the same values as this
            # object's values for all the unique field.
        
            lookup_kwargs = {}
            for field_name in unique_check:
                if field_name in self._meta.autopopulate:
                    # if a autopopulated field call the associated function to get the lookup value
                    lookup_kwargs[field_name] = self._meta.autopopulate[field_name](self.request, 
self.instance)
                else:
                    lookup_kwargs[field_name] = self.cleaned_data[field_name]
                
        
            qs = self.instance.__class__._default_manager.filter(**lookup_kwargs)

            # Exclude the current object from the query if we are editing an 
            # instance (as opposed to creating a new one)
            if self.instance.pk is not None:
                qs = qs.exclude(pk=self.instance.pk)
            
            # This cute trick with extra/values is the most efficient way to
            # tell if a particular query returns any results.
            if qs.extra(select={'a': 1}).values('a').order_by():
                model_name = capfirst(self.instance._meta.verbose_name)
            
                unique_check = [u for u in unique_check if u not in self._meta.autopopulate]
                # A unique field
                if len(unique_check) == 1:
                    field_name = unique_check[0]
                    field_label = self.fields[field_name].label
                    # Insert the error into the error dict, very sneaky
                    self._errors[field_name] = ErrorList([
                        _(u"%(model_name)s with this %(field_label)s already exists.") % \
                        {'model_name': unicode(model_name),
                         'field_label': unicode(field_label)}
                    ])
                # unique_together
                else:
                    field_labels = [self.fields[field_name].label for field_name in unique_check]
                    field_labels = get_text_list(field_labels, _('and'))
                    form_errors.append(
                        _(u"%(model_name)s with this %(field_label)s already exists.") % \
                        {'model_name': unicode(model_name),
                         'field_label': unicode(field_labels)}
                    )
            
                # Remove the data from the cleaned_data dict since it was invalid
                for field_name in unique_check:
                    if field_name not in self._meta.autopopulate:
                        del self.cleaned_data[field_name]
    
        if form_errors:
            # Raise the unique together errors since they are considered form-wide.
             raise ValidationError(form_errors)
        
class ModelAdmin(BaseModelAdmin):
    """
    Adds options to ModelAdmin that allow automatic filtering, 
    restricting and field-populating for non-superusers        
    """
    autofilter = None
    autofilter_choices = None
    autohide = None
    autopopulate = None
                    
    def get_fieldsets(self, request, obj=None):
        """Removes any autofilter fields from generated fieldsets"""
        fieldsets = super(ModelAdmin, self).get_fieldsets(request, obj=obj)
        if self.autopopulate and not request.user.is_superuser:
            for fieldset in fieldsets:
                fieldset[1]['fields'] = [f for f in fieldset[1]['fields'] if f not in 
self.autopopulate]
        return fieldsets
            
    def get_form(self, request, obj=None, **kwargs):
        """Configures model form to fill in autopopulate fields (removing those fields from the form)
            and restricts querysets for multiple-choice fields according to autofilter_choices."""
        if self.autopopulate and not request.user.is_superuser:
            defaults = {
                'form': AutopopulateModelForm,
                'exclude': self.autopopulate.keys() + list(kwargs.pop('exclude', [])),
            }
            # NOTE: exclude will override any self.exclude because of logic error in 
ModelAdmin.get_form
            # see django ticket #8999
            defaults.update(kwargs)
            
            Form = super(ModelAdmin, self).get_form(request, obj=obj, **defaults)
            # have to set these after the fact because superclass get_form will reject them in kwargs
            Form.request = request
            Form._meta.autopopulate = self.autopopulate
        else:
            Form = super(ModelAdmin, self).get_form(request, obj=obj, **kwargs)
            
        if self.autofilter_choices and not request.user.is_superuser:
            for fieldname, filters in self.autofilter_choices.iteritems():
                if fieldname in Form.base_fields:
                    field = Form.base_fields[fieldname]
                elif fieldname in Form.declared_fields:
                    field = Form.declared_fields[fieldname]
                else:
                    raise AttributeError("'%s' listed in autofilter_choices is not a valid field name" 
% fieldname)
                field.queryset = field.queryset.filter(**dict((fn, func(request, obj)) for fn, func in 
filters.iteritems()))
        
        return Form
        
    def changelist_view(self, request, *args, **kwargs):
        """
        The 'change list' admin view for this model. Hides any 'autohide' fields
        from the list_display, list_display_links, list_filter and search_fields 
        options for non-superusers.
        """
        if self.autohide and not (self.superuser_no_auto and request.user.is_superuser):
            self.list_display = [f for f in self.list_display if f not in self.autohide]
            self.list_display_links = [f for f in self.list_display_links if f not in self.autohide]
            self.list_filter = [f for f in self.list_filter if f not in self.autohide]
            self.search_fields = [f for f in self.search_fields if f not in self.autohide]

        return super(ModelAdmin, self).changelist_view(request, *args, **kwargs)

    def queryset(self, request):
        """Filters change list queryset by autofilter fields."""
        qs = super(ModelAdmin, self).queryset(request)
        if self.autofilter and not request.user.is_superuser:
            qs = qs.filter(**dict((field, func(request)) for field, func in 
self.autofilter.iteritems()))
        return qs

    def has_change_permission(self, request, obj=None):
        """Determines change permission dynamically based on autofilter option"""
        perm = super(ModelAdmin, self).has_change_permission(request, obj=obj)
        if obj is not None and self.autofilter and not request.user.is_superuser:
            for fieldname, func in self.autofilter.items():
                perm = perm and getattr(obj, fieldname) == func(request)
        return perm

    def has_delete_permission(self, request, obj=None):
        """Determines delete permission dynamically based on autofilter option"""
        perm = super(ModelAdmin, self).has_delete_permission(request, obj=obj)
        if obj is not None and self.autofilter and not request.user.is_superuser:
            for fieldname, func in self.autofilter.items():
                perm = perm and getattr(obj, fieldname) == func(request)
        return perm

class AutopopulateInlineFormSet(BaseInlineFormSet):
    """
    Subclasses BaseInlineFormSet to enable autopopulating of contained fields.
    Contained form should be an instance of AutopopulateModelForm.
    """
    def save_new(self, form, commit=True):
        """Saves and returns a new model instance for the given form."""
        kwargs = {self.fk.get_attname(): self.instance.pk}
        new_obj = self.model(**kwargs)
        for field, func in form._meta.autopopulate.iteritems():
            setattr(new_obj, field, func(form.request))
        return save_instance(form, new_obj, exclude=[self._pk_field.name], commit=commit)

    def save_existing(self, form, instance, commit=True):
        """Saves and returns an existing model instance for the given form."""
        for field, func in form._meta.autopopulate.iteritems():
            setattr(instance, field, func(form.request))
        return save_instance(form, instance, exclude=[self._pk_field.name], commit=commit)

class InlineModelAdmin(BaseInlineModelAdmin):
    """
    Adds options to inline admin classes that allow automatic filtering of multiple-choice fields
    and automatic field-population for non-superusers.
    """
    autopopulate = None
    autofilter_choices = None
    
    def get_formset(self, request, obj=None, **kwargs):
        """Configures formset to autopopulate fields according to the autopopulate option."""
        if self.autopopulate and not request.user.is_superuser:
            defaults = {
                'form': AutopopulateModelForm,
                'formset': AutopopulateInlineFormSet,
                'exclude': self.autopopulate.keys() + list(kwargs.pop('exclude', [])),
            }
            # NOTE: exclude will override any self.exclude because of logic error in 
ModelAdmin.get_formset 
            # see django ticket #8999
            defaults.update(kwargs)

            FormSet = super(InlineModelAdmin, self).get_formset(request, obj, **defaults)
            FormSet.form.request = request
            FormSet.form._meta.autopopulate = self.autopopulate
            
        else:
            FormSet = super(InlineModelAdmin, self).get_formset(request, obj, **kwargs)

        if self.autofilter_choices:
            for fieldname, filters in self.autofilter_choices.iteritems():
                if fieldname in FormSet.form.base_fields:
                    field = FormSet.form.base_fields[fieldname]
                elif fieldname in FormSet.form.declared_fields:
                    field = FormSet.form.declared_fields[fieldname]
                else:
                    raise AttributeError("'%s' listed in autofilter_choices is not a valid field name" 
% fieldname)
                field.queryset = field.queryset.filter(**dict((fn, func(request, obj)) for fn, func in 
filters.iteritems()))            
            
        return FormSet

class StackedInline(InlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'

class TabularInline(InlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'


