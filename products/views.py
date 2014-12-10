from org.tools import *
from products.models import Product,Comment,Order
from accounts.models import Lawyer,Client
from django.views import generic


# def index_view(request):
# 	latest_products_list = Product.objects.order_by('-publish_date')
# 	template = loader.get_template('products/index.html')
# 	context = RequestContext(request, {
# 		'latest_products_list': latest_products_list,
# 	})
# 	return HttpResponse(template.render(context))

# class IndexView(generic.ListView):
# 	template_name = 'products/index.html'
# 	context_object_name = 'latest_products_list'

# 	def get_queryset(self):
# 		return Product.objects.order_by('-publish_date')

def index_view(request):
	return response(request, 'products/index.html',
		latest_products_list=Product.objects.order_by('-publish_date') )

# class DetailView(generic.DetailView):
# 	model = Product
# 	template_name = 'products/detail.html'

# 	def get_context_data(self, **kwargs):
# 		context = super(DetailView, self).get_context_data(**kwargs)
# 		context['products_comments'] = Comment.objects.filter(product_id=self.object.id)
# 		return context

def detail_view(request, pk_product):
	product=get_object_or_404(Product, pk=pk_product)
	return response(request, 'products/detail.html',
		product=product,
		products_comments=Comment.objects.filter(product_id=pk_product))

def new_comment_view(request, pk):
	# print pk, request.POST['txt_comment']
	p = get_object_or_404(Product, pk=pk)
	try:
		# for k in dir(request.user):
		# 	if 'client' in k:
		# 		print repr(getattr(request.user,k)),getattr(request.user,k)
		comment = Comment.objects.create(text=request.POST['txt_comment'], user=request.user, product=p)
		comment.save()
	except :
		raise
		#return HttpResponseRedirect(reverse('index:index'))
	else:
		return HttpResponseRedirect(reverse('products:detail', args=(p.id,)))

def new_order_view(request, pk):
	# raise Http404
	p = get_object_or_404(Product, pk=pk)
	order = Order.objects.create( 
		client=request.user.client,
		product=p,
		lawyer=Lawyer.objects.filter(id=1),
		state=0,
		text=request.POST['text']
		)
	order.save()
	return empty #redirect('products:detail', args=(p.id))

