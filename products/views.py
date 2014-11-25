from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from products.models import Product

def index_view(request):
	latest_products_list = Product.objects.order_by('-publish_date')
	template = loader.get_template('products/index.html')
	context = RequestContext(request, {
		'latest_products_list': latest_products_list,
	})
	return HttpResponse(template.render(context))
