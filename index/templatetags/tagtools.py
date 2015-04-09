# -*- coding: utf-8 -*-
import re, logging
from org.tools import *
from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

logger = logging.getLogger('org.main')
logger_lambda = logging.getLogger('org.lambda')

@register.simple_tag
def query_assign(request,name,val):
	try:
		querystring=request.META['QUERY_STRING']
		pattern=r'\b{0}=[^&]*'.format(name)
		assignment='{0}={1}'.format(name,val)
		if re.search(pattern, querystring): return re.sub(pattern,assignment,querystring)
		else: return '{0}&{1}'.format(querystring,assignment)
	except: 
		logger_lambda.exception(u'lambda容错记录')
		return ''

TRANSACSERIAL_FILTER_FORMAT = \
	'<input name="{0}" type="hidden" value="{{0}}" />'.format(TRANSACSERIAL)

@register.filter(name='transacserial',is_safe=True)
@stringfilter
def transacserial_filter(transaction_name):
	try:
		return TRANSACSERIAL_FILTER_FORMAT.format(transacserial(transaction_name))
	except: 
		logger_lambda.exception(u'lambda容错记录')
		return ''

from org.antixss import antiXSS_BootstrapWYSIWYS
@register.filter(name='antixss',is_safe=True)
@stringfilter
def antixss_filter(html):
	try: return antiXSS_BootstrapWYSIWYS(html)
	except: return '<antiXSS_BootstrapWYSIWYS failure>'

from org.settings import DEFAULT_AVATAR_URL
@register.filter(name='avatarurl')
def avatarurl(user):
	from org.tools import get_role
	u = get_role(user)
	if type(u) is Client or type(u) is Lawyer:
		try:
			return u.avatar.url
		except Exception, e:
			return DEFAULT_AVATAR_URL
	else: return DEFAULT_AVATAR_URL

