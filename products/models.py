# -*- coding: utf-8 -*-
import random, hashlib, os
from datetime import datetime
from django.db import models, transaction
from django.contrib.auth.models import User
from org.types import Enum, CustomException

class Product(models.Model):
	name = models.CharField(u'产品名称', max_length=255)
	publish_date = models.DateTimeField(u'发布日期', default=datetime.now)
	description = models.TextField(u'产品描述', blank=True)
	price = models.DecimalField(u'定价', max_digits=16, decimal_places=3, default=0)
	include_html = models.CharField(u'静态html页面模板路径', max_length=255)

	class Meta:
		verbose_name = u'产品'
		verbose_name_plural = u'产品'

	def __unicode__(self):
		return self.name

class Comment(models.Model):
	user = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	text = models.TextField(u'正文')
	publish_date = models.DateTimeField(u'评论日期', auto_now=True)

	def __unicode__(self):
		return self.text[:20]

class EnumOrderState(Enum):
	UNPAID = 0
	IN_BUSINESS = 1
	FINISHED = 2
	CANCELLED = 3

def gen_order_serial():
	serial=[
		datetime.now().strftime("%Y%m%d%H%M%S"), # len = 14
		''.join(random.choice('QWERTYUIOPASDFGHJKLZXCVBNMZY') for i in xrange(4)), # len = 4
	]
	hashcode=hashlib.md5()
	for s in serial:
		hashcode.update(s)
	serial.append('H%s'%hashcode.hexdigest().upper()[:6]) # len = 7
	return ''.join(serial) # total len = 25

class Order(models.Model):
	client = models.ForeignKey('accounts.Client', on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	lawyer = models.ForeignKey('accounts.Lawyer', on_delete=models.SET_NULL, null=True, blank=True)
	serial = models.CharField(u'订单号', max_length=25, default=gen_order_serial, editable=False, unique=True)
	state = models.IntegerField(u'订单状态', default=EnumOrderState.UNPAID, choices=EnumOrderState.get_choices())
	text = models.TextField(u'订单备注', blank=True)
	publish_date = models.DateTimeField(u'创建日期', default=datetime.now)

	class Meta:
		verbose_name = u'订单'
		verbose_name_plural = u'订单'

	def is_unpaid(self):
		return self.state==EnumOrderState.UNPAID

	def is_in_business(self):
		return self.state==EnumOrderState.IN_BUSINESS

	def is_finished(self):
		return self.state==EnumOrderState.FINISHED

	@transaction.atomic
	def cancel(self):
		if self.state==EnumOrderState.UNPAID:
			self.state=EnumOrderState.CANCELLED
			self.save()
			return 1
		if self.state==EnumOrderState.IN_BUSINESS:
			self.state=EnumOrderState.CANCELLED
			self.save()
			return 2
		else: raise CustomException(u"状态转换异常")

	@transaction.atomic
	def finish(self):
		if self.state==EnumOrderState.UNPAID:
			self.state=EnumOrderState.FINISHED
			self.save()
			return 1
		if self.state==EnumOrderState.IN_BUSINESS:
			self.state=EnumOrderState.FINISHED
			self.save()
			return 2
		else: raise CustomException(u"状态转换异常")

	@transaction.atomic
	def start(self):
		if self.state==EnumOrderState.UNPAID:
			self.state=EnumOrderState.IN_BUSINESS
			self.save()
		else: raise CustomException(u"状态转换异常")

	def __unicode__(self):
		return u'{0}: {1}'.format(self.serial, self.product.name)

class OrderProcess(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	lawyer = models.ForeignKey('accounts.Lawyer', on_delete=models.SET_NULL, null=True)

	class Meta:
		unique_together = (("order", "lawyer"), )

class OrderDoc(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	title = models.CharField(u'文档标题', max_length=255, blank=True)
	doc = models.FileField(upload_to='order/doc/', max_length=255)
	publish_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title if self.title else os.path.basename(unicode(self.doc))

class OrderProcessContract(models.Model):
	orderprocess = models.ForeignKey(OrderProcess, on_delete=models.CASCADE)
	contract = models.ForeignKey('smartcontract.SmartContract', on_delete=models.SET_NULL, null=True)

	def __unicode__(self):
		return self.contract.name
		
class OrderContract(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	contract = models.ForeignKey('smartcontract.SmartContract', on_delete=models.SET_NULL, null=True)
	instance = models.ForeignKey('smartcontract.SmartContractInstance', on_delete=models.SET_NULL, null=True)

	def __unicode__(self):
		return self.contract.name
