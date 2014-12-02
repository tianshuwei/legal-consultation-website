from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views import generic
from products.models import Product,Comment
from django.core.urlresolvers import reverse

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
		print

		# Call the base implementation first to get a context
		context = super(DetailView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['products_comments'] = Comment.objects.filter(product_id=kwargs['object'].id)
		return context

def new_comment_view(request, pk):
	# print pk, request.POST['txt_comment']
	p = get_object_or_404(Product, pk=pk)
	try:
		# for k in dir(request.user):
		# 	if 'client' in k:
		# 		print repr(getattr(request.user,k)),getattr(request.user,k)
		comment = Comment.objects.create(comment=request.POST['txt_comment'], client=request.user.client, product=p)
		comment.save()
	except :
		raise
		#return HttpResponseRedirect(reverse('index:index'))
	else:
		return HttpResponseRedirect(reverse('products:detail', args=(p.id,)))

def new_order_view(request):
    raise Http404
