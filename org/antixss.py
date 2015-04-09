# -*- coding: utf-8 -*-
import bleach, os

def src_filter(name, value):
	if name == 'src':
		base, ext = os.path.splitext(value)
		return ext in ('.jpg', '.png', '.gif', '.jpeg')
	else: return False

options_BootstrapWYSIWYS = dict(
	tags = ['b', 'i', 'br', 'strike', 'u', 'ul', 'ol', 'li', 'div', 'font', 'img', 'span', 'blockquote'],

	attributes = {
		'div': ['style'],
		'font': ['face', 'size'],
		'img': src_filter,
		'span': ['style'],
		'blockquote': ['style'],
	},

	styles = [
		'text-align',
		'line-height',
		'color',
		'font-family',
		'line-height',
		'font-size',
		'margin',
		'padding',
		'border',
	])

def antiXSS_BootstrapWYSIWYS(text, strip=False):
	options=dict(options_BootstrapWYSIWYS, strip=strip)
	return bleach.clean(text, **options)
