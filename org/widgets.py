# -*- coding: utf-8 -*-
# see /usr/local/lib/python2.7/dist-packages/django/forms/widgets.py
from __future__ import unicode_literals
from itertools import chain
from django import forms
from django.forms.utils import flatatt, to_current_timezone
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.deprecation import RemovedInDjango18Warning
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import conditional_escape, format_html
from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe
from django.utils import formats, six
from django.utils.six.moves.urllib.parse import urljoin

class BootstrapWYSIWYG(forms.Widget):
	def render(self, name, value, attrs=None):
		if value is None: value = ''
		final_attrs = self.build_attrs(attrs, name=name)
		return format_html('<div{0}>\r\n{1}</div>', flatatt(final_attrs), force_text(value))

class BlogCategorySelect(forms.Select): 
	def render_options(self, choices, selected_choices):
		# Normalize to strings.
		selected_choices = set(force_text(v) for v in selected_choices)
		output = []
		for option_value, option_label in chain(self.choices, choices):
			if option_value==u'': continue
			elif option_label==u'默认': selected_choices = set([force_text(option_value)])
			if isinstance(option_label, (list, tuple)):
				output.append(format_html('<optgroup label="{0}">', force_text(option_value)))
				for option in option_label:
					output.append(self.render_option(selected_choices, *option))
				output.append('</optgroup>')
			else:
				output.append(self.render_option(selected_choices, option_value, option_label))
		return '\n'.join(output)
