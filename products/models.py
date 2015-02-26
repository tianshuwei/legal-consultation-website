# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User

class Product(models.Model):
	name = models.CharField(max_length=255,default='')
	publish_date = models.DateTimeField('date published',auto_now=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=16, decimal_places=3,default=0)

	def __unicode__(self):
		return self.name

class Comment(models.Model):
	user = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	text = models.TextField()
	publish_date = models.DateTimeField('date published',auto_now=True)

	def __unicode__(self):
		return self.text[:20]

class Order(models.Model):
	client = models.ForeignKey('accounts.Client')
	product = models.ForeignKey(Product)
	lawyer = models.ForeignKey('accounts.Lawyer')
	state = models.IntegerField(default=0) # 0=UNPAID 1=IN BUSINESS 2=FINISHED
	text = models.TextField()
	publish_date = models.DateTimeField('date published',auto_now=True)

	def is_unpaid(self):
		return self.state==0

	def is_in_business(self):
		return self.state==1

	def is_finished(self):
		return self.state==2

	def __unicode__(self):
		return self.text[:20]

