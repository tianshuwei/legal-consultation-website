# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from blogs.models import BlogSettings, BlogCategory

"""
Fields in User
	username
	password
	email
	first_name
	last_name
"""

class ClientManager(models.Manager):
	@transaction.atomic
	def register(self, username, **profile):
		user=User.objects.create_user(username,**profile)
		user.save()
		client=Client.objects.create(user=user)
		client.save()
		return client

class Client(models.Model):
	user = models.OneToOneField(User)
	balance = models.DecimalField(max_digits=16, decimal_places=3,default=0)
	points = models.IntegerField(default=0)
	#comments = models.ManyToManyField("products.Product", through="products.Comment", through_fields=("client","product"), related_name="c_p_comments")

	objects = ClientManager()

	def __unicode__(self):
		return self.user.username

class LawyerManager(models.Manager):
	@transaction.atomic
	def register(self, username, **profile):
		user=User.objects.create_user(username,**profile)
		user.save()
		lawyer=Lawyer.objects.create(user=user)
		lawyer.save()
		BlogSettings.objects.create(lawyer=lawyer).save()
		BlogCategory.objects.create(lawyer=lawyer, name=u"默认").save()
		return lawyer

class Lawyer(models.Model):
	user = models.OneToOneField(User)
	balance = models.DecimalField(max_digits=16, decimal_places=3,default=0)
	blacklist = models.BooleanField(default=False)
	score = models.IntegerField(default=0)
	remarks = models.ManyToManyField(Client, through="Remark", through_fields=("lawyer","client"), related_name="c_l_remarks")
	questions = models.ManyToManyField(Client, through="Question", through_fields=("lawyer","client"), related_name="c_l_questions")

	objects = LawyerManager()

	def __unicode__(self):
		return self.user.username

class Remark(models.Model):
	lawyer = models.ForeignKey(Lawyer)
	client = models.ForeignKey(Client)
	grade = models.IntegerField(default=0)
	publish_date = models.DateTimeField('date published',auto_now=True)

	def __unicode__(self):
		return str(self.grade)

class Question(models.Model):
	lawyer = models.ForeignKey(Lawyer)
	client = models.ForeignKey(Client)
	title = models.CharField(max_length=255,default='')
	description = models.TextField()
	publish_date = models.DateTimeField('date published',auto_now=True)

	def __unicode__(self):
		return self.title

class Question_text(models.Model):
	question = models.ForeignKey(Question)
	user_flag = models.IntegerField(default=0)
	text = models.TextField()
	publish_date = models.DateTimeField('date published',auto_now=True)

	def __unicode__(self):
		return self.text[:20]

