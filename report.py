#!/usr/bin/env python

"""MTV Report Jan 2015 (C) Alex"""

import os, sys, re, linecache, itertools, operator
r_urlref = re.compile(r"'(\w+:\w+)'")
SECTION = lambda name: '[\x1B[1;34;40m%s\x1B[0m]' % name
F = lambda fname, line=None: '\x1B[0;35;40m%s\x1B[0;36;40m:%d\x1B[0m' % (fname, line) if line else '\x1B[0;35;40m%s\x1B[0m' % fname
LINE = lambda l: '\x1B[0;36;40m:%d\x1B[0m' % l
V = lambda name: '<\x1B[5;33;40m%s\x1B[0m>' % name
U = lambda urlref: '\x1B[0;31;40m<no name>\x1B[0m' if not urlref else(
		urlref if urlref in url_refs_templates else '\x1B[0;31;40m%s\x1B[0m' % urlref)

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

class Application(object):
	def __init__(self, app_name):
		super(Application, self).__init__()
		self.name = app_name
		mk_urlref = lambda name: '{0}:{1}'.format(app_name,name) if name else None
		self.url_mappings = [(mk_urlref(url.name), url.callback.__name__, url.regex.pattern) 
			for url in __import__(app_name+'.urls').urls.urlpatterns]
		self.url_refs = {
			'tests': set(m.group(1) for m in grep(r_urlref,os.path.join(app_name,'tests.py'))),
			'templates': set(m.group(1) for ext, fname in find(['.html','.js'], os.path.join(app_name,'templates')) for m in grep(r_urlref,fname)),
		}
		f_views = os.path.join(app_name,'views.py')
		def func_len(si):
			r_funcbody = re.compile(r'^(\W.*|\n`)')
			for l in xrange(si+1, 100000):
				if not r_funcbody.match(linecache.getline(f_views, l)):
					return l-si
		r_deffunc = re.compile(r'^def\s+(\w+)\(.*')
		self.views = [{
			'file': f_views,
			'line': view[0],
			'func_name': view[1],
			'range': xrange(view[0], view[0]+func_len(view[0])),
			'urls': [(urlref,pattern) 
				for urlref, func_name, pattern in self.url_mappings if func_name==view[1]],
		} for view in (
			(l,m.group(1)) for l,m in filter(lambda (l,m): m,
				((l+1,r_deffunc.match(line)) for l,line in enumerate(linecache.getlines(f_views)))))]
		r_POST = re.compile(r'\bPOST\b')
		r_TODO = re.compile(r'#\s*TODO\s+(.*)\s*$')
		for view in self.views:
			for l in view['range']:
				if r_POST.search(linecache.getline(f_views, l)):
					view['POST'] = True; break
			else: view['POST'] = False
			view['TODO']=[m.group(1) for m in (
				r_TODO.search(linecache.getline(f_views, l)) for l in view['range']) if m]

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
		f_models=os.path.join(app_name,'models.py')
		self.models = [{
			'name': obj.__name__,
			'doc': obj.__doc__,
			'file': f_models, 
			'members': filter(bool,(member(i) for i in vars(obj).iteritems())),
		} for obj_name,obj in vars(__import__(app_name+'.models').models).iteritems()
			if type(obj) is django.db.models.base.ModelBase and obj_name not in ['User']]
		self.f_models=f_models
		self.models_todo=[(l,m.group(1)) for l,m in linematch(r_TODO, f_models)]
		linecache.clearcache()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "org.settings")
import org.settings
apps = [Application(app) for app in org.settings.INSTALLED_APPS if os.path.isdir(app) and os.path.exists(os.path.join(app,'urls.py'))]
print __doc__
print 'Apps:', [app.name for app in apps]

url_refs_templates = reduce(operator.ior, [a.url_refs['templates'] for a in apps]+[
	set(m.group(1) for ext, fname in find(['.html', '.js'], 'templates') for m in grep(r_urlref,fname))])

@section('Model Layer')
def __model():
	print 'Relation Summary:'
	for a in apps:
		for model in a.models:
			print '\t%(doc)s'%model
	for a in apps:
		print 'Relations (%s): %d'%(a.name,len(a.models))
		for model in a.models:
			print '\t%(doc)s'%model
			for member in model['members']:
				print '\t\t%s %s'%member
	# admin 2 -admin.py
	# function reference 2 -views.py

# @section('Template Layer')
# def __template():
	# block hierarchy 3
	# source compactness 2
	# id usage 2

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

	isolated_urls = filter(lambda (urlref, func_name, pattern):urlref not in url_refs_templates,url_mappings)
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
def l_todo():
	for a in apps:
		for view in (view for view in a.views if view['TODO']):
			print '\t%(F)s %(V)s' % dict(view, F=F(view['file'],view['line']), V=V(view['func_name']))
			for i,todo in enumerate(view['TODO']):
				print '\t%d. %s' % (i+1,todo)
		if a.models_todo:
			print '\t%s' % F(a.f_models)
			for i,(l,todo) in enumerate(a.models_todo):
				print '\t%d. %s %s' % (i+1,todo,LINE(l))

if __name__ == '__main__':
	for section in sections:
		print SECTION(section['title'])
		section['func']()
	print 'EOF'
