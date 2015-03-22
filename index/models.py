# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from org.types import Enum

class TransactionRecord(models.Model):
	title = models.CharField(max_length=80, blank=True, default='')
	serial = models.CharField(max_length=20)
	result = models.CharField(max_length=20)
	message = models.CharField(max_length=120, blank=True)
	publish_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title

	def success(self, msg):
		self.result, self.message = 'success', msg
		self.save()

	def error(self, msg):
		self.result, self.message = 'error', msg
		self.save()

class SiteActivityManager(models.Manager):
	pass
	# @transaction.atomic
	# def notify_new_user(self, user):
	# 	r = self.create(
	# 		title=user.username,
	# 		tags='register'
	# 	)
	# 	r.save()

class EnumSiteActivityState(Enum):
	NEW = 0
	VIEWED = 1

class SiteActivity(models.Model):
	title = models.CharField(max_length=255)
	tags = models.CharField(max_length=255, blank=True, default='')
	state = models.IntegerField(default=EnumSiteActivityState.NEW, choices=EnumSiteActivityState.get_choices())
	publish_date = models.DateTimeField(auto_now=True, null=True)

	objects = SiteActivityManager()