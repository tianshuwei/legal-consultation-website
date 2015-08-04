# -*- coding: utf-8 -*-
from org.tools import *
from products.models import Product,Comment,Order,EnumOrderState
from accounts.models import Lawyer,Client,Activity
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
	Activity.objects.profile_new_product_comment(request.user, p)
	return redirect('products:detail', pk_product=p.id)

@login_required
def new_order_view(request, pk_product):
	if request.method=='POST':
		rec=recorded(request, 'products:new_order')
		try:
			client=request.user.client
			product=Product.objects.get(pk=pk_product)
			# TODO 用户中心点击支付时再支付，以后再调，原来if先去掉了
			# a=client.minus_balance(product.price)
			with transaction.atomic():
				order = Order.objects.create( 
					client=client,
					product=product,
					lawyer=Lawyer.objects.get(pk=request.POST['lawyer_id']),
					state=EnumOrderState.UNPAID,
					text=request.POST['text']
				)
				order.save()
		except Product.DoesNotExist:
			messages.error(request,u'产品不存在')
			rec.error(u'{0}产品不存在'.format(request.user.username))
			# TODO 提交者不是客户/产品不存在/违反完整性约束约束 这些异常要区分开记录
			# TODO 取消注释下面一行可以看Exception类型，except里面加以区分
			#traceback.print_exc() # 最后要注释掉或删掉，不要保留这一行
			# TODO rec.error(...
		except Exception, e: 
			messages.error(request, u'订单提交失败')
			# TODO 必要时调用 handle_illegal_access 参考org/tools.py中的文档
			return response_jquery({ 'success': False })
		else: 
			messages.success(request, u'订单提交成功')
			rec.success(u'{0} 订单提交成功 {1}'.format(request.user.username, order.serial))
			return response_jquery({ 'success': True })
	else: raise Http404

@login_required
def order_detail_view(request, pk_order):
	# TODO 按照上面new_order_view修改
	rec=recorded(request, 'products:order_detail')
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		try:
			if request.user.client==order.client:
				order.text=request.POST['text']
				order.save()
			else: raise Exception
		except: messages.error(request, u'备注修改失败')
		else: 
			messages.success(request, u'备注修改成功')
			rec.success(u'{0} 订单备注修改成功 {1}'.format(request.user.username, order.serial))
		return redirect('accounts:order_detail', pk_order=pk_order)
	else: return response(request, 'accounts/order_detail.html', order=order)

@login_required
def order_delete_view(request, pk_order):
	# TODO 按照上面new_order_view修改
	rec=recorded(request, 'products:order_delete')
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		try:
			if request.user.client==order.client: 
				serial_d=order.serial
				a=order.cancel()
				if a==2:
					order.client.add_balance(order.product.price)
			else: raise Exception			
		except: 
			messages.error(request, u'取消订单失败')	
			return response_jquery({'r':'false'})
		else: 
			messages.success(request, u'取消订单成功')
			rec.success(u'{0} 订单删除成功 {1}'.format(request.user.username, serial_d))
			return response_jquery({'r':'success'})
	else: raise Http404

@login_required
def order_pay_view(request, pk_order):
	rec=recorded(request, 'products:order_pay')
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':	
		try:
			if request.user.client==order.client:
				a=order.client.minus_balance(order.product.price)
				if a==1:
					order.start()
					messages.success(request, u'订单付款成功')
					rec.success(u'{0} 订单付款成功 {1}'.format(request.user.username, order.serial))
					return response_jquery({'r':'success'})
				else:
					messages.error(request, u'账户余额不足')
					rec.success(u'{0} 订单付款余额不足 {1}'.format(request.user.username, order.serial))
					return response_jquery({'r':'balance_false'})
		except:
			messages.error(request, u'订单取消失败')
			return response_jquery({'r':'false'})

@login_required
def order_complete_view(request, pk_order):
	rec=recorded(request, 'products:order_complete')
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		try:
			if request.user.client==order.client: 
				serial_d=order.serial
				a=order.finish()
			else: raise Exception			
		except: 
			messages.error(request, u'完成订单失败')	
			return response_jquery({'r':'false'})
		else: 
			messages.success(request, u'完成订单成功')
			rec.success(u'{0} 订单完成成功 {1}'.format(request.user.username, serial_d))
			return response_jquery({'r':'success'})
	else: raise Http404