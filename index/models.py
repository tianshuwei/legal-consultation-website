# -*- coding: utf-8 -*-
from django.db import models, transaction

class TransactionRecord(models.Model):
	title = models.CharField(max_length=80,default='')
	serial = models.CharField(max_length=20,default='')
	result = models.CharField(max_length=20,default='')
	message = models.CharField(max_length=120,default='')
	publish_date = models.DateTimeField('date published',auto_now=True)

	def __unicode__(self):
		return self.title

	def __call__(self, msg):
		self.result, self.message = ('success' if u'成功' in msg else 'error'), msg
		self.save()
		return msg

