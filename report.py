#!/usr/bin/env python

"""
Jan 2015 (C) Alex
"""

import os, sys, re, linecache, itertools

def SECTION(name):
	print '[\x1B[1;34;40m%s\x1B[0m]' % name

def F(fname, line=None):
	if line: return '\x1B[0;35;40m%s\x1B[0;36;40m:%d\x1B[0m' % (fname, line)
	else: return '\x1B[0;35;40m%s\x1B[0m' % fname

def V(name):
	return '<\x1B[1;37;40m%s\x1B[0m>' % name

def U(urlref):
	if not urlref: return '\x1B[0;31;40m<no name>\x1B[0m'
	if urlref in url_refs_templates: return urlref
	else: return '\x1B[0;31;40m%s\x1B[0m' % urlref

def grep(pattern, fname):
	with open(fname,'rb') as f:
		return pattern.finditer(f.read())

def linecount(fname):
	with open(fname, 'rb') as f:
		return sum(b.count('\n') for b in itertools.takewhile(bool,(f.read(65536) for i in itertools.count())))

def mk_index(app):
	urlpatterns = __import__(app+'.urls').urls.urlpatterns
	mk_urlref = lambda name: '{0}:{1}'.format(app,name) if name else None
	url_mappings = [(mk_urlref(url.name), url.callback.__name__, url.regex.pattern) for url in urlpatterns]
	r_urlref = re.compile(r"'(\w+:\w+)'")
	url_refs = {
		'tests': set(m.group(1) for m in grep(r_urlref,os.path.join(app,'tests.py'))),
		'templates': set(m.group(1) for dirpath, dirnames, filenames in 
			os.walk(os.path.join(app,'templates')) for f in filenames if os.path.splitext(f)[1] in ['.html','.js']
				for m in grep(r_urlref,os.path.join(dirpath,f))),
	}
	linecache.clearcache()
	f_views = os.path.join(app,'views.py')
	def func_len(si):
		r_funcbody = re.compile(r'^(\W.*|\n`)')
		for l in xrange(si+1, 100000):
			if not r_funcbody.match(linecache.getline(f_views, l)):
				return l-si
	r_deffunc = re.compile(r'^def\s+(\w+)\(.*')
	view_defs = [{
		'file': f_views,
		'line': view[0],
		'func_name': view[1],
		'range': xrange(view[0], view[0]+func_len(view[0])),
		'urls': [(urlref,pattern) 
			for urlref, func_name, pattern in url_mappings if func_name==view[1]],
	} for view in (
		(l,m.group(1)) for l,m in filter(lambda (l,m): m,
			((l+1,r_deffunc.match(line)) for l,line in enumerate(linecache.getlines(f_views)))))]
	r_POST = re.compile(r'\bPOST\b')
	r_TODO = re.compile(r'#\s*TODO\s+(.*)\s*$')
	for view in view_defs:
		for l in view['range']:
			if r_POST.search(linecache.getline(f_views, l)):
				view['POST'] = True; break
		else: view['POST'] = False
		view['TODO']=[m.group(1) for m in (
			r_TODO.search(linecache.getline(f_views, l)) for l in view['range']) if m]
	linecache.clearcache()
	return url_mappings, url_refs, view_defs

def get_colors(fname):
	r_color = re.compile(r'((#[0-9a-fA-F]{6})\b|(#[0-9a-fA-F]{3})\b|(rgb\([0-9, %]+\)))')
	return set([m.group(1) for m in grep(r_color,fname)])

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "org.settings")
	import org.settings
	myapps = [app for app in org.settings.INSTALLED_APPS if os.path.isdir(app) and os.path.exists(os.path.join(app,'urls.py'))]
	print 'Apps examined:', myapps
	
	SECTION('Models Quality Report')
	# relation summary 1
	# admin 2 -admin.py
	# function reference 2 -views.py
	# test coverage 2 -tests.py
	# todo list 1
	# constraint 999

	# SECTION('Templates Quality Report')
	# block hierarchy 3
	# source compactness 2
	# id usage 2

	SECTION('Views Quality Report')
	url_mappings = list() 
	url_refs_templates = set()
	todo_list = dict()

	# Test coverage
	for app in myapps:
		_url_mappings, _url_refs, view_defs = mk_index(app)
		url_mappings+=_url_mappings
		url_refs_templates|=_url_refs['templates']
		view4post = [view for view in view_defs 
			for urlref,pattern in view['urls'] if view['POST']]
		uncovered = [dict(view,urlref=urlref) for view in view_defs 
			for urlref,pattern in view['urls'] if view['POST'] and urlref and urlref not in _url_refs['tests']]
		print 'Test coverage (%s): %.1f%%'%(app,(1.0-float(len(uncovered))/float(len(view4post)) if len(view4post) else 1.0)*100.0)
		if uncovered:
			print 'Views not covered by unit test:', len(uncovered)
			for view in uncovered:
				print '\t%(F)s %(urlref)s -> %(V)s' % dict(view, F=F(view['file'],view['line']), V=V(view['func_name']))
		todo_list[app] = filter(lambda view:view['TODO'], view_defs)

	# Isolated URLs
	r = filter(lambda (urlref, func_name, pattern):urlref not in url_refs_templates,url_mappings)
	if r:
		print 'Isolated URLs:', len(r)
		for urlref, func_name, pattern in r:
			print '\t%s -> %s  /%s/'%(U(urlref), V(func_name), pattern)

	# Todo list
	print 'Todo list'
	for app in todo_list:
		for view in todo_list[app]:
			print '\t%(file)s:%(line)d %(V)s' % dict(view, V=V(view['func_name']))
			for i,todo in enumerate(view['TODO']):
				print '\t%d. %s' % (i+1,todo)

	SECTION('Site Structure')
	print 'URL Mappings', len(url_mappings)
	for urlref, func_name, pattern in url_mappings:
		print '\t%s -> %s  /%s/'%(U(urlref), V(func_name), pattern)

	SECTION('CSS Summary')
	for dirpath, dirnames, filenames in os.walk('.'):
		for f in filenames:
			base,ext = os.path.splitext(f)
			if ext == '.css':
				print F(os.path.join(dirpath,f))
				print '\tColor set:', get_colors(os.path.join(dirpath,f))

	SECTION('Source Summary')
	exts = ['.py','.html','.js','.css']
	src_wc = {ext:list([0]*2) for ext in exts}
	for dirpath, dirnames, filenames in os.walk('.'):
		for f in filenames:
			base,ext = os.path.splitext(f)
			if ext in exts:
				src_wc[ext][0] += 1
				src_wc[ext][1] += linecount(os.path.join(dirpath,f))
	for ext in src_wc:
		print ext
		print '\t', src_wc[ext][0], "files"
		print '\t', src_wc[ext][1], "lines"
	print 'total lines:', sum((src_wc[ext][1] for ext in src_wc))

	print 'EOF'
