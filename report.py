#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MTV Report
Copyright 2015 Alex Yang
"""

import os, sys, re, linecache, itertools, operator, org.settings
r_urlref = re.compile(r"'(\w+:\w+)'")
r_template_extends=re.compile(r'{%\s*extends\s+(?P<quo>(\"|\'))(?P<val>.*?)(?P=quo)\s*%}')
r_template_include=re.compile(r'{%\s*include\s+(?P<quo>(\"|\'))(?P<val>.*?)(?P=quo)\s*%}')
r_template_blocks=re.compile(r'{%\s*block\s+(?P<val>.*?)\s*%}')
r_template_ids=re.compile(r'id=(?P<quo>(\"|\'))(?P<val>.*?)(?P=quo)')
if 1:
	SECTION = lambda name: '[\x1B[1;34;40m%s\x1B[0m]' % name
	F = lambda fname, line=None: '\x1B[0;35;40m%s\x1B[0;36;40m:%d\x1B[0m' % (fname, line) if line else '\x1B[0;35;40m%s\x1B[0m' % fname
	LINE = lambda l: '\x1B[0;36;40m:%d\x1B[0m' % l
	V = lambda name: '<\x1B[5;33;40m%s\x1B[0m>' % name
	U = lambda urlref: '\x1B[0;31;40m<no name>\x1B[0m' if not urlref else(
		urlref if urlref in url_refs_templates else '\x1B[0;31;40m%s\x1B[0m' % urlref)
	RELATION_NAME = lambda R, f_admin: '\x1B[0;34;40m%s\x1B[0m'%R if list(grep(re.compile(''.join([r'\b',R,r'\b'])), f_admin)) else R
	RELATION_ATTR = lambda attr, foreign_keys: '\x1B[4;37;40m%s\x1B[0m'%attr if attr.endswith('_id') and attr[:-3] in foreign_keys else (
		'\x1B[1;37;40mid\x1B[0m' if attr=='id' else attr)
	BASE = lambda name: '\x1B[0;32;40m%s\x1B[0m'%name
	TREE_SP=u"   "; TREE_LAST=u"└──"; TREE_PARENT=u'│'; TREE_MID=u'├'
else: # remove r'\\x1B\[[\d;]+m'
	SECTION = lambda name: '[%s]' % name
	F = lambda fname, line=None: '%s:%d' % (fname, line) if line else '%s' % fname
	LINE = lambda l: ':%d' % l
	V = lambda name: '<%s>' % name
	U = lambda urlref: '<no name>' if not urlref else(
		urlref if urlref in url_refs_templates else '%s' % urlref)
	RELATION_NAME = lambda R, f_admin: '%s'%R if list(grep(re.compile(''.join([r'\b',R,r'\b'])), f_admin)) else R
	RELATION_ATTR = lambda attr, foreign_keys: '%s'%attr if attr.endswith('_id') and attr[:-3] in foreign_keys else (
		'id' if attr=='id' else attr)
	BASE = lambda name: '%s'%name
	TREE_SP=u"   "; TREE_LAST=u"`--"; TREE_PARENT=u'|'; TREE_MID=u'|'

sections = list()
r_section = re.compile(r'(\w)_(\w+)')
def section(title, **options):
	def _section(func):
		r = dict(title=title, func=func)
		m = r_section.match(func.__name__)
		if m: r = dict(r, short=m.group(1) if m.group(1)!='_' else m.group(2)[0], long=m.group(2))
		sections.append(dict(r, **options))
		return func
	return _section

def find(exts, path='.'):
	for dirpath, dirnames, filenames in os.walk(path):
		for f in filenames:
			base, ext = os.path.splitext(f)
			if ext in exts: yield ext, os.path.join(dirpath,f)

def grep(pattern, fname):
	with open(fname,'rb') as f:
		return pattern.finditer(f.read())

def linematch(pattern, fname):
	with open(fname,'rb') as f:
		for l,line in enumerate(f.xreadlines()):
			m=pattern.search(line)
			if m: yield l+1, m

def linecount(fname):
	with open(fname, 'rb') as f:
		return sum(b.count('\n') for b in itertools.takewhile(bool,(f.read(65536) for i in itertools.count())))

def tree(x, width=65535):
	r = list(); foo = lambda x,w:[x[p:p+w] for p in xrange(0,len(x),w)]
	for d,i in x:
		if d>0:
			j=foo(i,width-len(TREE_SP)*d)
			r+=map(lambda k:''.join([TREE_SP*(d-1),TREE_LAST,k]),j[:1])+map(lambda k:''.join([TREE_SP*d,k]),j[1:])
		else: r+=foo(i,width)
		p = len(TREE_SP)*(d-1)
		if r[-1][p]==TREE_LAST[0]:
			for j in reversed(xrange(len(r)-1)):
				if r[j][p] == TREE_SP[0]: r[j] = TREE_PARENT.join([r[j][:p],r[j][p+1:]])
				elif r[j][p] == TREE_LAST[0]: r[j] = TREE_MID.join([r[j][:p],r[j][p+1:]])
				else: break 
	return r

class Application(object):
	def __init__(self, app_name):
		super(Application, self).__init__()
		self.name = app_name
		mk_urlref = lambda name: '{0}:{1}'.format(app_name,name) if name else None
		self.url_mappings = [(mk_urlref(url.name), url.callback.__name__, url.regex.pattern) 
			for url in __import__(app_name+'.urls').urls.urlpatterns]
		self.d_templates = os.path.join(app_name, 'templates')
		self.url_refs = {
			'tests': set(m.group(1) for m in grep(r_urlref,os.path.join(app_name,'tests.py'))),
			'templates': set(m.group(1) for ext, fname in find(['.html','.js'], self.d_templates) for m in grep(r_urlref,fname)),
		}
		self.f_views = os.path.join(app_name,'views.py')
		def func_len(si):
			r_funcbody = re.compile(r'^(\W.*|\n`)')
			for l in itertools.count(si+1):
				if not r_funcbody.match(linecache.getline(self.f_views, l)):
					return l-si
		r_deffunc = re.compile(r'^def\s+(\w+)\(.*')
		self.views = [{
			'file': self.f_views,
			'line': view[0],
			'func_name': view[1],
			'range': xrange(view[0], view[0]+func_len(view[0])),
			'urls': [(urlref,pattern) 
				for urlref, func_name, pattern in self.url_mappings if func_name==view[1]],
		} for view in (
			(l,m.group(1)) for l,m in filter(lambda (l,m): m,
				((l+1,r_deffunc.match(line)) for l,line in enumerate(linecache.getlines(self.f_views)))))]
		r_POST = re.compile(r'\bPOST\b')
		r_TODO = re.compile(r'#\s*TODO\s+(.*)\s*$')
		for view in self.views:
			for l in view['range']:
				if r_POST.search(linecache.getline(self.f_views, l)):
					view['POST'] = True; break
			else: view['POST'] = False
			view['TODO']=[m.group(1) for m in (
				r_TODO.search(linecache.getline(self.f_views, l)) for l in view['range']) if m]

		import django.db, types
		type_code = {
			django.db.models.fields.related.ReverseSingleRelatedObjectDescriptor: 'S',
			django.db.models.fields.related.ForeignRelatedObjectsDescriptor: 'F',
			django.db.models.fields.related.ReverseManyRelatedObjectsDescriptor: 'M',
			types.FunctionType: 'f',
		}
		def member((member_name,m)):
			t = type(m)
			if not member_name.startswith('_') and t in type_code: return type_code[t], member_name
			elif t is django.db.models.manager.ManagerDescriptor:
				manager_name = m.manager.__class__.__name__
				if manager_name != 'Manager': return 'O', manager_name
		self.f_models=os.path.join(app_name,'models.py')
		self.models = [{
			'name': obj.__name__,
			'doc': obj.__doc__,
			'file': self.f_models, 
			'members': filter(bool,(member(i) for i in vars(obj).iteritems())),
		} for obj_name,obj in vars(__import__(app_name+'.models').models).iteritems()
			if type(obj) is django.db.models.base.ModelBase and obj_name not in ['User']]
		self.models_todo=[(l,m.group(1)) for l,m in linematch(r_TODO, self.f_models)]
		linecache.clearcache()

		self.templates = [{
			'file': fname,
			'template': os.path.relpath(fname, self.d_templates),
			'extends': [m.group('val') for m in grep(r_template_extends,fname)][:1] or [None], 
			'include': [m.group('val') for m in grep(r_template_include,fname)], 
			'blocks': [m.group('val') for m in grep(r_template_blocks,fname)],
			'ids': [m.group('val') for m in grep(r_template_ids,fname)],
		} for ext, fname in find(['.html','.js'], self.d_templates)]

@section('Copyrights and licenses')
def l_copyright():
	r_LICENSE = re.compile(r'(?i)(licensed\x20under|copyright.*\d{4})')
	llen=lambda x: x if x>=0 else 0
	for ext, fname in find(['.py','.js','.css','.html']):
		for l,m in linematch(r_LICENSE, fname):
			print F(fname,l), m.string.strip()[:llen(120-len(fname))]

@section('Model Layer')
def __model():
	print 'Entity Summary:', sum(len(a.models) for a in apps)
	r_relation = re.compile(r'(\w+)\((.*)\)')
	for a in apps:
		f_admin = os.path.join(a.name,'admin.py')
		for model in a.models:
			m = r_relation.match(model['doc'])
			foreign_keys = [attr for t,attr in model['members'] if t=='S']
			print '\t%s(%s)'%(
				RELATION_NAME(m.group(1),f_admin),
				',\x20'.join(itertools.starmap(RELATION_ATTR,((attr,foreign_keys) for attr in m.group(2).split(',\x20')))))
	# for a in apps:
	# 	print 'Relations (%s): %d'%(a.name,len(a.models))
	# 	for model in a.models:
	# 		print '\t%(doc)s'%model
	# 		for member in model['members']:
	# 			print '\t\t%s %s'%member

@section('Template Layer')
def __template():
	r = reduce(operator.add, [a.templates for a in apps])
	r_dict = {t['template']:t for t in r}
	for ext, fname in find(['.html','.js'], 'templates'):
		_template = os.path.relpath(fname, 'templates')
		if _template not in r_dict:
			template={
				'file': fname,
				'template': os.path.relpath(fname, 'templates'),
				'extends': [m.group('val') for m in grep(r_template_extends,fname)][:1] or [None], 
				'include': [m.group('val') for m in grep(r_template_include,fname)], 
				'blocks': [m.group('val') for m in grep(r_template_blocks,fname)],
				'ids': [m.group('val') for m in grep(r_template_ids,fname)],
			}
			r_dict[_template]=template
			r.append(template)
	for template in r:
		base = template['extends'][0]
		extends = r_dict[base] if base in r_dict else base
		template['extends'] = extends
		if extends and type(extends) is dict:
			if 'extended_by' in extends: template['extends']['extended_by'].append(template)
			else: extends['extended_by']=list([template])
		template['include_set'] = template['include']
		template['include'] = map(lambda t:r_dict[t] if t in r_dict else t, template['include'])
	includes = reduce(operator.ior, (set(t['include_set']) for t in r))
	print 'Template Hierarchy'
	def walk_templates(i,d=0):
		def block_def(block, i):
			if i['extends'] and type(i['extends']) is dict: 
				return False if block in i['extends']['blocks'] else block_def(block, i['extends'])
			else: return True
		r = ',\x20'.join(filter(lambda b:block_def(b,i),i['blocks'])+i['include_set'])
		if r: r=''.join(['(',r,')'])
		if 'extended_by' in i and i['extended_by']:
			yield d,BASE(i['template'])+r
			for t in i['extended_by']:
				for j in walk_templates(t, d+1): yield j
		else: yield d,i['template']+r
	roots=filter(lambda t:t['extends']==None and t['template'] not in includes,r)
	for i in tree(reduce(operator.add,(list(walk_templates(root,d=1)) for root in roots)), width=120):
		print i

@section('View Layer')
def __view():
	for a in apps:
		view4post = [view for view in a.views for urlref,pattern in view['urls'] if view['POST']]
		uncovered = [dict(view,urlref=urlref) for view in a.views 
			for urlref,pattern in view['urls'] if view['POST'] and urlref and urlref not in a.url_refs['tests']]
		print 'Test coverage (%s): %.1f%%'%(a.name,(1.0-float(len(uncovered))/float(len(view4post)) if len(view4post) else 1.0)*100.0)
		if uncovered:
			print 'Views not covered by unit test:', len(uncovered)
			for view in uncovered:
				print '\t%(F)s %(urlref)s -> %(V)s' % dict(view, F=F(view['file'],view['line']), V=V(view['func_name']))

@section('Site Structure')
def w_site():
	url_mappings = [url_mapping for a in apps for url_mapping in a.url_mappings]
	print 'URL Mappings', len(url_mappings)
	for urlref, func_name, pattern in url_mappings:
		print '\t%s -> %s  /%s/'%(U(urlref), V(func_name), pattern)
	isolated_urls = filter(lambda (urlref, func_name, pattern):urlref and urlref not in url_refs_templates,url_mappings)
	print 'Isolated URLs:', len(isolated_urls)
	for urlref, func_name, pattern in isolated_urls:
		print '\t%s -> %s  /%s/'%(U(urlref), V(func_name), pattern)

@section('CSS Summary')
def __css():
	r_color = re.compile(r'((#[0-9a-fA-F]{6})\b|(#[0-9a-fA-F]{3})\b|(rgb\([0-9, %]+\)))')
	for ext, fname in find(['.css']):
		print F(fname)
		print '\tColor set:', set([m.group(1) for m in grep(r_color,fname)])

@section('Source Summary')
def __source():
	exts = ['.py','.html','.js','.css']
	src_wc = {ext:list([0]*2) for ext in exts}
	for ext, fname in find(exts):
		src_wc[ext][0] += 1
		src_wc[ext][1] += linecount(fname)
	for ext in src_wc:
		print ext
		print '\t', src_wc[ext][0], "files"
		print '\t', src_wc[ext][1], "lines"
	print 'total lines:', sum((src_wc[ext][1] for ext in src_wc))

@section('Todo list')
def z_todo():
	for a in apps:
		for view in (view for view in a.views if view['TODO']):
			print '\t%(F)s %(V)s' % dict(view, F=F(view['file'],view['line']), V=V(view['func_name']))
			for i,todo in enumerate(view['TODO']):
				print '\t%d. %s' % (i+1,todo)
		if a.models_todo:
			print '\t%s' % F(a.f_models)
			for i,(l,todo) in enumerate(a.models_todo):
				print '\t%d. %s %s' % (i+1,todo,LINE(l))

def get_options():
	import argparse
	parser = argparse.ArgumentParser()
	for section in sections:
		parser.add_argument('-%s'%section['short'], '--%s'%section['long'],
			action='store_true', dest=section['long'], default=False, 
			help='show %s section'%section['title'])
	parser.add_argument('--all',
		action='store_true', dest='all_sections', default=False, 
		help='show all sections')
	# option conflict regex /^def (x_\w+|__x\w*)\(\)/
	return parser.parse_args()

if __name__ == '__main__':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "org.settings")
	apps = [Application(app) for app in org.settings.INSTALLED_APPS if os.path.isdir(app) and os.path.exists(os.path.join(app,'urls.py'))]
	print __doc__
	print 'Apps:', [app.name for app in apps]
	url_refs_templates = reduce(operator.ior, [a.url_refs['templates'] for a in apps]+[
		set(m.group(1) for ext, fname in find(['.html', '.js'], 'templates') for m in grep(r_urlref,fname))])
	options = get_options()
	for section in sections:
		if options.all_sections or getattr(options, section['long']):
			print SECTION(section['title'])
			section['func']()
	print 'EOF'
