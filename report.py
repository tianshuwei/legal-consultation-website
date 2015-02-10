#!/usr/bin/env python
import os, sys, re, linecache

def mk_index(app):
	urlpatterns = __import__(app+'.urls').urls.urlpatterns
	mk_urlref = lambda name: '{0}:{1}'.format(app,name) if name else None
	url_mappings = [(mk_urlref(url.name), url.callback.__name__, url.regex.pattern) for url in urlpatterns]
	r_urlref = re.compile(r"'(\w+:\w+)'")
	url_refs = {
		'tests': set(m.group(1) for line in 
			linecache.getlines(os.path.join(app,'tests.py')) for m in r_urlref.finditer(line)),
		'templates': set(m.group(1) for dirpath, dirnames, filenames in 
			os.walk(os.path.join(app,'templates')) for f in filenames if os.path.splitext(f)[1] in ['.html','.js']
				for line in linecache.getlines(os.path.join(dirpath,f)) for m in r_urlref.finditer(line)),
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

if __name__ == "__main__":
	print '[Views Quality Report]'
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "org.settings")
	import org.settings
	myapps = [app for app in org.settings.INSTALLED_APPS if os.path.isdir(app) and os.path.exists(os.path.join(app,'urls.py'))]
	print 'Apps examined:', myapps

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
				print '\t%(file)s:%(line)d %(urlref)s -> <%(func_name)s>' % view
		todo_list[app] = filter(lambda view:view['TODO'], view_defs)

	# Isolated URLs
	r = filter(lambda (urlref, func_name, pattern):urlref not in url_refs_templates,url_mappings)
	if r:
		print 'Isolated URLs:', len(r)
		for urlref, func_name, pattern in r:
			print '\t%s -> <%s>  /%s/'%(urlref or '<no name>', func_name, pattern)

	# Todo list
	print 'Todo list'
	for app in todo_list:
		for view in todo_list[app]:
			print '\t%(file)s:%(line)d <%(func_name)s>' % view
			for i,todo in enumerate(view['TODO']):
				print '\t%d. %s' % (i+1,todo)

	print 'EOF'
