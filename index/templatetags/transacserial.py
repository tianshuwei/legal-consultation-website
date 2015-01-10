# -*- coding: utf-8 -*-
from org.tools import *
from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

TRANSACSERIAL_FILTER_FORMAT = \
	'<input name="{0}" type="hidden" value="{{0}}" />'.format(TRANSACSERIAL)

@register.filter(name='transacserial',is_safe=True)
@stringfilter
def transacserial_filter(transaction_name):
	return TRANSACSERIAL_FILTER_FORMAT.format(transacserial(transaction_name))
