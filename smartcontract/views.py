from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse

def test_render_view(request):
	template = loader.get_template('smartcontract/test.html')
	context = RequestContext(request, {
		# 'latest_products_list': None,
	})
	return HttpResponse(template.render(context))

