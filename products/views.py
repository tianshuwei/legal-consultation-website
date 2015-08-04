# -*- coding: utf-8 -*-
from org.tools import *
from products.models import Product,Comment,Order,EnumOrderState,OrderProcess,OrderDoc,OrderProcessContract,OrderContract
from accounts.models import Lawyer,Client,Activity
from smartcontract.models import SmartContract
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
					# lawyer=Lawyer.objects.get(pk=request.POST['lawyer_id']),
					state=EnumOrderState.UNPAID,
					# text=request.POST['text']
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
			messages.success(request, u'订单提交成功 订单号{0}'.format(order.serial))
			rec.success(u'{0} 订单提交成功 {1}'.format(request.user.username, order.serial))
			return response_jquery({ 'success': True })
	else: raise Http404

@login_required
def order_detail_view(request, pk_order):
	# TODO 按照上面new_order_view修改
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		rec=recorded(request, 'products:order_detail')
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
	else: return response(request, 'accounts/order_detail.html', order=order, 
		EN_ORDERPROCESS=True, # 启用Order-Lawyer间的1:n联系OrderProcess
		orderdocuploadform = OrderDocUploadForm()
		)

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
					rec.error(u'{0} 订单付款余额不足 {1}'.format(request.user.username, order.serial))
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

@login_required
def process_new_order_view(request):
	rec=recorded(request, 'products:order_process')
	if request.method=='POST':
		try:
			serial = request.POST['serial']
			order = Order.objects.get(serial=serial)
			lawyer = get_role(request.user)
			assert type(lawyer) is Lawyer
			with transaction.atomic():
				order_process = OrderProcess.objects.create(
					order=order,
					lawyer=lawyer
				)
				order_process.save()
		except:
			messages.error(request, u'加入订单失败')
			rec.error(u'{0} 加入订单失败 {1}'.format(request.user.username, serial))
		else:
			messages.success(request, u'加入订单成功')
			rec.success(u'{0} 加入订单成功 {1}'.format(request.user.username, serial))			
		return redirect('accounts:order_list')
	else: raise Http404

class OrderDocUploadForm(forms.ModelForm):
	class Meta:
		model = OrderDoc
		fields = ['title', 'doc']

@login_required
def upload_order_doc(request, pk_order):
	if request.method=='POST':
		try:
			with transaction.atomic():
				order_doc = OrderDocUploadForm(request.POST, request.FILES).save(commit=False)
				order_doc.order = get_object_or_404(Order, pk=pk_order)
				order_doc.save()
		except: messages.error(request, u'上传失败')
		else: messages.success(request, u'上传成功')
		return redirect('products:order_detail', pk_order=pk_order)
	else: raise Http404

@login_required
def delete_order_doc(request, pk_orderdoc):
	if request.method=='POST':
		try:
			with transaction.atomic():
				order_doc = get_object_or_404(OrderDoc, pk=pk_orderdoc)
				pk_order = order_doc.order.id
				order_doc.delete()
		except:
			messages.error(request, u'删除失败')
			return redirect('accounts:order_list')
		else:
			messages.success(request, u'删除成功')
			return redirect('products:order_detail', pk_order=pk_order)
	else: raise Http404

@login_required
def query_order_contract_templates(request, pk_order):
	# from smartcontract.models import SmartContract
	key = request.GET['q'].strip() if 'q' in request.GET else ''
	return response(request, 'products/order_contract_search_result.mod.html',
		order_contracts=SmartContract.objects.filter(name__contains=key))

@login_required
def add_order_contract_template(request, pk_order):
	if request.method=='POST':
		try:
			pk_contract = request.POST['pk_contract']
			contract = get_object_or_404(SmartContract, pk=pk_contract)
			order = get_object_or_404(Order, pk=pk_order)
			lawyer = get_role(request.user)
			assert type(lawyer) is Lawyer
			order_process = OrderProcess.objects.filter(lawyer=lawyer).get(order=order)
			with transaction.atomic():
				order_contract = OrderProcessContract.objects.create(
					orderprocess = order_process,
					contract = contract
				)
				order_contract.save()
		except:
			return response_jquery({"ok":False})
			# messages.error(request, u'添加失败')
		else:
			return response_jquery({"ok":True})
			# messages.success(request, u'添加成功')
		# return redirect('products:order_detail', pk_order=pk_order)

@login_required
def list_orderprocess_contract_templates(request, pk_order):
	order = get_object_or_404(Order, pk=pk_order)
	u = get_role(request.user)
	if type(u) is Lawyer:
		lawyer = u
		order_process = OrderProcess.objects.filter(lawyer=lawyer).get(order=order)
		return response(request, 'products/orderprocess_contract_list.mod.html',
			order = order,
			order_contracts=order_process.orderprocesscontract_set.all())
	elif type(u) is Client:
		return response(request, 'products/orderprocess_contract_list.mod.html',
			order = order,
			order_contracts=SmartContract.objects.raw(
			"""SELECT DISTINCT 
					smartcontract_smartcontract.id AS "id", 
					smartcontract_smartcontract.name AS "name", 
					(products_ordercontract.id IS NOT NULL) AS "filledin"
				FROM  
					products_orderprocesscontract
					INNER JOIN products_orderprocess ON 
						orderprocess_id=products_orderprocess.id
					LEFT JOIN products_ordercontract ON 
						products_ordercontract.order_id=products_orderprocess.order_id AND
						products_ordercontract.contract_id=products_orderprocesscontract.contract_id
					INNER JOIN smartcontract_smartcontract ON 
						smartcontract_smartcontract.id=products_orderprocesscontract.contract_id
				WHERE 
					products_orderprocesscontract.contract_id=smartcontract_smartcontract.id AND 
					products_orderprocess.order_id=%s;""", [pk_order]))

@login_required
def remove_order_contract_template(request, pk_OPcontract):
	if request.method=='POST':
		try:
			order_contract = get_object_or_404(OrderProcessContract, pk=pk_OPcontract)
			order_contract.delete()
		except: return response_jquery({"ok":False})
		else: return response_jquery({"ok":True})
	else: raise Http404

@login_required
def order_contract_form(request, pk_order):
	order = get_object_or_404(Order, pk=pk_order)
	if 'pk_contract' in request.GET:
		contract = get_object_or_404(SmartContract, pk=request.GET['pk_contract'])
	else: raise Http404
	if request.method=='POST':
		import json
		from smartcontract.models import SmartContractInstance
		content = json.dumps({k:request.POST[k] for k in request.POST if k.startswith('var_')})
		try:
			with transaction.atomic():
				instance = SmartContractInstance.objects.create(
					contract = contract,
					user = request.user,
					data = content
				)
				instance.save()
				order_contract = OrderContract.objects.create(
					order = order,
					contract = contract,
					instance = instance
				)
				order_contract.save()
		except: traceback.print_exc()
		else: print 1
		raise Http404
	else:
		from smartcontract.views import steps_spliter
		return response(request, 'products/order_contract_form.html',
			contract=contract, order=order,
			steps=steps_spliter(filter(bool,(i.strip() for i in contract.config.replace('\r','').split('\n')))))
