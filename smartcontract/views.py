# -*- coding: utf-8 -*-
from urllib import quote
#
from org.tools import *

mk_disposition = lambda filename: '\x20'.join([ # according to RFC 6266
	'attachment;',
	'filename="%s";' % quote(filename),
	"filename*=%(charset)s'%(lang)s'%(value)s" % {
		'charset': 'utf-8',
		'lang': '',
		'value': quote(filename)
	}, 
])

mk_random = lambda l: ''.join(random.choice('QWERTYUIOPASDFGHJKLZXCVBNMZY') for i in xrange(l))

def test_render_view(request):
	# TODO Unkown error: DocTemplate
	from org.docxrenderer import DocxTemplate
	if request.method=='POST':
		template=DocxTemplate(request.FILES['docxtemplate'])
		r=template.get_vars()
		if request.POST['test']=='scan':
			return response(request, 'smartcontract/renderer_test.html',
				variables=[{'name':var,'count':r[var]} for var in sorted(r)])
		elif request.POST['test']=='render':
			for var in r: r[var]=u'["{0}" - 中文 English]'.format(var)
			doc=template.render(**r)
			r=HttpResponse(content_type='application/octet-stream')
			r['Content-Disposition'] = mk_disposition("docxrenderer 测试%s.docx" % mk_random(4))
			doc.save(r)
			return r
		else: raise Http404
	else: return response(request, 'smartcontract/renderer_test.html')
