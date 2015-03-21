# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from org.types import Enum

class TransactionRecord(models.Model):
	title = models.CharField(max_length=80,default='')
	serial = models.CharField(max_length=20,default='')
	result = models.CharField(max_length=20,default='')
	message = models.CharField(max_length=120,default='')
	publish_date = models.DateTimeField('date published',auto_now=True)

	def __unicode__(self):
		return self.title

	def success(self, msg):
		self.result, self.message = 'success', msg
		self.save()

	def error(self, msg):
		self.result, self.message = 'error', msg
		self.save()

class EnumSiteActivityState(Enum):
	NEW = 0
	VIEWED = 1

class SiteActivity(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255)
	state = models.IntegerField(default=EnumSiteActivityState.NEW, choices=EnumSiteActivityState.get_choices())
	publish_date = models.DateTimeField(auto_now=True, null=True)
