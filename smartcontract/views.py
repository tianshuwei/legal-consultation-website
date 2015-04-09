# -*- coding: utf-8 -*-
import re
from urllib import quote
from org.tools import *
from smartcontract.models import SmartContract

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

def conf_spliter(re_sep, func_content):
	def spliter(lines):
		seps = [(i,m.group(1)) for i,m in enumerate(map(re_sep.match, lines)) if m]
		item = lambda name, content: { 'content': func_content(content), 'name': name }
		if seps:
			for i in xrange(len(seps)-1): yield item(seps[i][1], lines[seps[i][0]+1:seps[i+1][0]])
			yield item(seps[-1][1], lines[seps[-1][0]+1:])
	return spliter

r_ATTR = re.compile(r'(\w+)\s*=\s*(.*)')
def var_attr(v):
	m = r_ATTR.search(v)
	if m:
		name, val = m.group(1), m.group(2)
		if name=='values': val = val.split(',')
		return name, val
	else: return None, None

steps_spliter = conf_spliter(re.compile(r'^\s*>+\s*(.*)\s*$'), 
	conf_spliter(re.compile(r'^\s*\[\s*(\w+)\s*\]\s*$'),
		lambda x:{name:val for name, val in map(var_attr,x) if name}))

def test_render_form_view(request, pk_contract):
	contract = SmartContract.objects.get(id=pk_contract)
	return response(request, 'smartcontract/render_form.html', contract=contract, 
		steps=steps_spliter(filter(bool,(i.strip() for i in contract.config.replace('\r','').split('\n')))))

def test_pdf_view(request, pk_contract):
	contract = SmartContract.objects.get(id=pk_contract)
	return response(request, 'smartcontract/pdf.js.html')

def index_view(request):
	return response(request,'smartcontract/index.html')

def download_0409_view(request, pk_contract):
	# TODO Unkown error: DocTemplate
	from org.docxrenderer import DocxTemplate
	if request.method=='POST':
		contract = SmartContract.objects.get(id=pk_contract)
		template = DocxTemplate(contract.template)
		r = template.get_vars()
		# print contract.template.url
		# print dir(contract.template)

		"""
		{'companyName': 3, 'percent': 1, 'companyAdd': 1, 'boss': 2, 'employee': 2, 'idCode': 1, 'time': 1, 'duration': 1, 'employeeAddress': 1}
		<QueryDict: {u'var_companyName': [u'jlkfds'], u'var_idCode': [u'cdks'], u'var_employeeAddress': [u'kjcewkl'], u'var_duration': [u'43'], u'var_time': [u'654'], u'var_percent': [u'23'], u'var_companyAdd': [u'djsal'], u'var_boss': [u'fds'], u'csrfmiddlewaretoken': [u'nFFgoXGHTIFZHiPiuQwECMZ5w53xCIu5'], u'var_employee': [u'jckldw']}>

		"""

		for var in r: 
			q_var = 'var_'+var
			if q_var in request.POST:
				r[var]= request.POST[q_var]
		doc=template.render(**r)
		r=HttpResponse(content_type='application/octet-stream')
		import os
		# print quote(unicode(os.path.basename(contract.template.path)))
		# TODO 文件名编码转换
		r['Content-Disposition'] = mk_disposition("contract.docx")
		doc.save(r)
		return r

		# return redirect('smartcontract:detail', pk_contract=1)
	else: raise Http404
