# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from org.types import Enum, CustomException

class Product(models.Model):
	name = models.CharField(max_length=255,default='')
	publish_date = models.DateTimeField(auto_now=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=16, decimal_places=3, default=0)

	def __unicode__(self):
		return self.name

class Comment(models.Model):
	user = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	text = models.TextField()
	publish_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.text[:20]

class EnumOrderState(Enum):
	UNPAID = 0
	IN_BUSINESS = 1
	FINISHED = 2
	CANCELLED = 3

def gen_order_serial():
	return '='*25

class Order(models.Model):
	client = models.ForeignKey('accounts.Client')
	product = models.ForeignKey(Product)
	lawyer = models.ForeignKey('accounts.Lawyer')
	serial = models.CharField(max_length=25, default=gen_order_serial, editable=False)
	state = models.IntegerField(default=EnumOrderState.UNPAID)
	text = models.TextField(blank=True)
	publish_date = models.DateTimeField(auto_now=True)

	def is_unpaid(self):
		return self.state==EnumOrderState.UNPAID

	def is_in_business(self):
		return self.state==EnumOrderState.IN_BUSINESS

	def is_finished(self):
		return self.state==EnumOrderState.FINISHED

	@transaction.atomic
	def cancel(self):
		if self.state==EnumOrderState.UNPAID or self.state==EnumOrderState.IN_BUSINESS:
			self.state=EnumOrderState.CANCELLED
			self.save()
		else: raise CustomException(u"状态转换异常")

	@transaction.atomic
	def finish(self):
		if self.state==EnumOrderState.IN_BUSINESS:
			self.state=EnumOrderState.FINISHED
			self.save()
		else: raise CustomException(u"状态转换异常")

	@transaction.atomic
	def start(self):
		if self.state==EnumOrderState.UNPAID:
			self.state=EnumOrderState.IN_BUSINESS
			self.save()
		else: raise CustomException(u"状态转换异常")

	def __unicode__(self):
		return u'{0}: {1}'.format(self.serial, self.product.name)

