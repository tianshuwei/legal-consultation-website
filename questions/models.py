# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from datetime import datetime
from org.types import Enum
from org.settings import EN_FULLTEXTSEARCH, POSTGRESQL
from org.dbtools import rawsql

class EnumQuestionState(Enum):
	OPEN = 0
	CLOSED = 1	

class QuestionManager(models.Manager):
	use_for_related_fields = True

	def search(self, query):
		if EN_FULLTEXTSEARCH and POSTGRESQL:
			return self.extra(where=["title@@%s or description@@%s"], params=[query,query]).order_by('-publish_date')
		else:
			return self.filter(Q(title__contains=query)|Q(description__contains=query)).order_by('-publish_date')

	def get_latest_questions(self):
		return self.order_by('-publish_date')[:6]

	def get_popular_questions(self):
		return self.order_by('-clicks')[:6]

class Question(models.Model):
	lawyer = models.ForeignKey('accounts.Lawyer', null=True)
	client = models.ForeignKey('accounts.Client')
	title = models.CharField(u'问题标题', max_length=255)
	clicks = models.IntegerField(u'问题点击量', default=0, editable=False)
	description = models.TextField(u'问题描述', blank=True)
	publish_date = models.DateTimeField(u'提问日期', default=datetime.now)
	state = models.IntegerField(u'问题状态', default=EnumQuestionState.OPEN, choices=EnumQuestionState.get_choices())

	objects = QuestionManager()

	class Meta:
		verbose_name = u'问题咨询'
		verbose_name_plural = u'问题咨询'

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
	user_flag = models.IntegerField(u'追问/回答', default=EnumUser_flag.ANSWER, choices=EnumUser_flag.get_choices())
	text = models.TextField(u'正文')
	publish_date = models.DateTimeField(u'发布日期', default=datetime.now)

	def __unicode__(self):
		return self.text[:20]
