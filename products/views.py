# -*- coding: utf-8 -*-
from org.tools import *
from products.models import Product,Comment,Order,EnumOrderState
from accounts.models import Lawyer,Client
from django.views import generic

def index_view(request):
	return response(request, 'products/index.html',
		latest_products_list=Product.objects.order_by('-publish_date') )

def detail_view(request, pk_product):
	product=get_object_or_404(Product, pk=pk_product)
	return response(request, 'products/detail.html',
		product=product,
		products_comments=Comment.objects.filter(product_id=pk_product),
		lawyers=Lawyer.objects.all())

@login_required
def new_comment_view(request, pk_product):
	p = get_object_or_404(Product, pk=pk_product)
	comment = Comment.objects.create(text=request.POST['txt_comment'], user=request.user, product=p)
	comment.save()
	return redirect('products:detail', pk_product=p.id)

@login_required
def new_order_view(request, pk_product):
	try:
		cl=request.user.client
		pr=Product.objects.get(pk=pk_product)
		a=cl.minus_balance(pr.price)
		if(a==1):
			Order.objects.create( 
				client=cl,
				product=pr,
				lawyer=Lawyer.objects.get(pk=request.POST['lawyer_id']),
				state=EnumOrderState.UNPAID,
				text=request.POST['text']
			).save()
		else:
			raise Exception
	except Exception, e: 
		traceback.print_exc() # DEBUG_ONLY
		messages.error(request, u'订单提交失败')
		return response_jquery({ 'success': False })
	else: 
		messages.success(request, u'订单提交成功')
		return response_jquery({ 'success': True })

@login_required
def order_detail_view(request, pk_order):
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		try:
			if request.user.client==order.client:
				order.text=request.POST['text']
				order.save()
			else: raise Exception
		except: messages.error(request, u'备注修改失败')
		else: messages.success(request, u'备注修改成功')
		return redirect('accounts:order_detail', pk_order=pk_order)
	else: return response(request, 'accounts/order_detail.html', order=order)

@login_required
def order_delete_view(request, pk_order): # TODO use post in template
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		try:
			if request.user.client==order.client: order.delete()
			else: raise Exception			
		except: messages.error(request, u'取消订单失败')	
		else: messages.success(request, u'取消订单成功')
		return redirect('accounts:usercenter')
	else: raise Http404
