# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from org.types import Enum

class EnumQuestionState(Enum):
	OPEN = 0
	CLOSED = 1	

class Question(models.Model):
	lawyer = models.ForeignKey('accounts.Lawyer', null=True)
	client = models.ForeignKey('accounts.Client')
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	publish_date = models.DateTimeField(auto_now=True)
	state = models.IntegerField(default=EnumQuestionState.OPEN, choices=EnumQuestionState.get_choices())

	def __unicode__(self):
		return self.title

	def finish(self):
		self.state=EnumQuestionState.CLOSED
		self.save()

class EnumQuestionState(Enum):
	OPEN = 0
	CLOSED = 1

class EnumUser_flag(Enum):
	ANSWER = 0
	ASK = 1

class Question_text(models.Model):
	replier = models.ForeignKey(User, null=True)
	question = models.ForeignKey(Question)
	user_flag = models.IntegerField(default=EnumUser_flag.ANSWER, choices=EnumUser_flag.get_choices())
	text = models.TextField()
	publish_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.text[:20]
