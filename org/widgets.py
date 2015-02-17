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
	def __init__(self, attrs=None):
		super(BootstrapWYSIWYG, self).__init__(attrs)
 
	def render(self, name, value, attrs=None):
		if value is None: value = ''
		final_attrs = self.build_attrs(attrs, name=name)
		return format_html('<div{0}>\r\n{1}</div>', flatatt(final_attrs), force_text(value))
