from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from products.models import Product

# def index_view(request):
# 	latest_products_list = Product.objects.order_by('-publish_date')
# 	template = loader.get_template('products/index.html')
# 	context = RequestContext(request, {
# 		'latest_products_list': latest_products_list,
# 	})
# 	return HttpResponse(template.render(context))

class IndexView(generic.ListView):
	template_name = 'products/index.html'
	context_object_name = 'latest_products_list'

	def get_queryset(self):
		return Product.objects.order_by('-publish_date')

class DetailView(generic.DetailView):
	model = Product
	template_name = 'products/detail.html'

