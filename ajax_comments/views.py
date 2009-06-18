from django import http
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.contrib import comments
from django.contrib.comments import signals
from django.utils import simplejson
from django.conf import settings 
from django.utils.hashcompat import sha_constructor

def generate_security_hash(content_type, object_pk, timestamp):
    info = (content_type, object_pk, timestamp, settings.SECRET_KEY) 
    return sha_constructor("".join(info)).hexdigest() 

def ajax_comment_post(request, next=None):
    """
    Post a comment.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """

    # Require POST
    if request.method != 'POST':
        return http.HttpResponseNotAllowed(["POST"])

    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if "name" not in data:
	    name = request.user.get_full_name()
	    if name == "":
		name = request.user.username 
            data["name"] = name
        if "email" not in data:
            data["email"] = request.user.email
	    if data["email"] == '':
		data["email"] = 'no@email.com'
#    data["is_public"] = False
    if not 'comment' in data:
	data['comment']=' ';
    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        error = "Missing content_type or object_pk field." 
        status = simplejson.dumps({'status': 'debug', 'error': error})
        return http.HttpResponse(status, mimetype="application/json")
    try:
	model = ContentType.objects.get(id=ctype)
#        model = models.get_comment_model(*ctype.split(".", 1))
#        target = model._default_manager.get(pk=object_pk)
	target = model.get_object_for_this_type(pk=object_pk)
    except TypeError:
        error = "Invalid content_type value: %r" % escape(ctype)
        status = simplejson.dumps({'status': 'debug', 'error': error})
        return http.HttpResponse(status, mimetype="application/json")
    except AttributeError:
        error = "The given content-type %r does not resolve to a valid model." % escape(ctype)
        status = simplejson.dumps({'status': 'debug', 'error': error})
        return http.HttpResponse(status, mimetype="application/json")
    except ObjectDoesNotExist:
        error = "No object matching content-type %r and object PK %r exists." % (escape(ctype), escape(object_pk))
        status = simplejson.dumps({'status': 'debug', 'error': error})
        return http.HttpResponse(status, mimetype="application/json")

    timestamp = data["timestamp"]
    data["security_hash"] = generate_security_hash(ctype, object_pk, timestamp)

    # Do we want to preview the comment?
    preview = data.get("submit", "").lower() == "preview" or \
              data.get("preview", None) is not None


    # Check security information
#    if form.security_errors():
    if request.user.is_anonymous():
# 	error = "The comment form failed security verification: %s" % escape(str(form.security_errors()))
	error = "You are not logged in!"
        status = simplejson.dumps({'status': 'debug', 'error': error})
        return http.HttpResponse(status, mimetype="application/json")



    # Construct the comment form
    form = comments.get_form()(target, data=data)

    # If there are errors or if we requested a preview show the comment
    if form.errors or preview:
        error = ""
        for e in form.errors:
            error += "Error in the %s field: %s" % (e, form.errors[e])
        status = simplejson.dumps({'status': 'error', 'error': error})
        return http.HttpResponse(status, mimetype="application/json")


    # Otherwise create the comment
#    CommentModel = comments.get_model()
    if 'comment_pk' in data:
	CommentModel = comments.get_model()
	comment_pk = int(data['comment_pk'])
	try:
		comment= CommentModel.objects.get(pk=comment_pk)
	except ObjectDoesNotExist:
                status = simplejson.dumps({'status': "success",'pk': comment_pk,'remove':True})
                return http.HttpResponse(status, mimetype="application/json")
	if 'remove' in data: # security check
		if ((request.user.has_perm('comments.delete_comment') and request.user==comment.user)  or (request.user.has_perm('comments.can_manage'))):
			comment_pk=comment.pk
			comment.delete()
			status = simplejson.dumps({'status': "success",'pk': comment_pk,'remove':True})
			return http.HttpResponse(status, mimetype="application/json")
		elif (request.user.has_perm('comments.change_comment') and request.user==comment.user):
			comment.is_public = False
			comment.is_removed = True
		else:
			error = "You don't have permissions to do this!"
			status = simplejson.dumps({'status': 'debug', 'error': error})
		        return http.HttpResponse(status, mimetype="application/json")
	else:
		if not ((request.user.has_perm('comments.change_comment') and request.user==comment.user)  or (request.user.has_perm('comments.can_manage'))):
                        error = "You don't have permissions to do this!"
                        status = simplejson.dumps({'status': 'debug', 'error': error})
                        return http.HttpResponse(status, mimetype="application/json")
		comment.comment=data['comment']
        	if request.user.has_perm('comments.add_comment'):
        	    comment.is_public = True
        	else:
        	    comment.is_public = False

    else:
	comment = form.get_comment_object()
	comment.ip_address = request.META.get("REMOTE_ADDR", None)
	if request.user.is_authenticated():
            comment.user = request.user
	if request.user.has_perm('comments.add_comment'):
    	    comment.is_public = True
        else:
	    comment.is_public = False
    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(comment)

    for (receiver, response) in responses:
        if response == False:
            error = "comment_will_be_posted receiver %r killed the comment" % receiver.__name__
            status = simplejson.dumps({'status': 'debug', 'error': error})
            return http.HttpResponse(status, mimetype="application/json")

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(comment)
    if comment.is_removed == True:
	status = simplejson.dumps({'status': "success",'pk': comment.pk,'remove':comment.is_removed})
    else:
	status = simplejson.dumps({'status': "success",'pk': comment.pk,'is_public':comment.is_public})
    return http.HttpResponse(status, mimetype="application/json")



