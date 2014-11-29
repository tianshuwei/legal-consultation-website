from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views import generic
from products.models import Product,Comment

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

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(DetailView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['products_comments'] = Comment.objects.all()
		return context

def new_comment_view(request, pk):
	print pk, request.POST['txt_comment']
	return HttpResponse('template.render(context)')




