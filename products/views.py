from org.tools import *
from products.models import Product,Comment,Order
from accounts.models import Lawyer,Client
from django.views import generic

def index_view(request):
	return response(request, 'products/index.html',
		latest_products_list=Product.objects.order_by('-publish_date') )

def detail_view(request, pk_product):
	product=get_object_or_404(Product, pk=pk_product)
	return response(request, 'products/detail.html',
		product=product,
		products_comments=Comment.objects.filter(product_id=pk_product))

@login_required
def new_comment_view(request, pk_product):
	p = get_object_or_404(Product, pk=pk_product)
	comment = Comment.objects.create(text=request.POST['txt_comment'], user=request.user, product=p)
	comment.save()
	return redirect('products:detail', pk_product=p.id)

@login_required
def new_order_view(request, pk_product):
	try:
		Order.objects.create( 
			client=request.user.client,
			product=Product.objects.get(pk=pk_product),
			lawyer=Lawyer.objects.filter(id=1),
			state=0,
			text=request.POST['text']
		).save()
	except Exception, e: 
		traceback.print_exc() # DEBUG_ONLY
		messages.error(request, u'订单提交失败')
		return response_jquery({ 'success': False })
	else: 
		messages.success(request, u'订单提交成功')
		return response_jquery({ 'success': True })

