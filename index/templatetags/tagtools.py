# -*- coding: utf-8 -*-
import re
from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.simple_tag
def query_assign(request,name,val):
	try:
		querystring=request.META['QUERY_STRING']
		pattern=r'\b{0}=[^&]*'.format(name)
		assignment='{0}={1}'.format(name,val)
		if re.search(pattern, querystring): return re.sub(pattern,assignment,querystring)
		else: return '{0}&{1}'.format(querystring,assignment)
	except: return ''
