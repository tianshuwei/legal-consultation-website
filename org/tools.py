from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render

def message(request,msg=None):
	"""	
	To get message in template:
		{% if request.session.result_text %}
			{{ request.session.result_text }}
		{% endif %}
	"""
	if msg: request.session['result_text'] = msg
	else: del request.session['result_text']

def redirect(url_ref,**kwargs):
	return HttpResponseRedirect(reverse(url_ref, kwargs = kwargs))

def response(request, template_name, **context):
	return HttpResponse(loader.get_template(template_name).render(RequestContext(request, context)))

def checkf(exp, default=None):
	try: return exp()
	except: return default

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import get_object_or_404
