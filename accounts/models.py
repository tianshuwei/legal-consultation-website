# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from org.types import Enum

class ClientManager(models.Manager):
	@transaction.atomic
	def register(self, username, **profile):
		user=User.objects.create_user(username,**profile)
		user.save()
		client=Client.objects.create(user=user)
		client.save()
		return client

class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	balance = models.DecimalField(max_digits=16, decimal_places=3, default=0)
	points = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to='avatar.client/', max_length=255, null=True)
	# comments = models.ManyToManyField("products.Product", through="products.Comment", through_fields=("client","product"), related_name="c_p_comments")

	objects = ClientManager()

	class Meta:
		verbose_name = u'客户'
		verbose_name_plural = u'客户'

	def __unicode__(self):
		return self.user.username

	@transaction.atomic
	def minus_points(self): 
		if self.points<=0: return -1
		self.points-=1
		self.save()
		return 1

	@transaction.atomic
	def minus_balance(self,count): 
		if self.balance<count: return -1
		self.balance-=count
		self.save()
		return 1


class LawyerManager(models.Manager):
	@transaction.atomic
	def register(self, username, **profile):
		user=User.objects.create_user(username,**profile)
		user.save()
		lawyer=Lawyer.objects.create(user=user)
		lawyer.save()
		from blogs.models import BlogSettings, BlogCategory, EnumBlogCategoryState
		BlogSettings.objects.create(lawyer=lawyer).save()
		BlogCategory.objects.create(lawyer=lawyer, name=u"默认", state=EnumBlogCategoryState.SYSTEM).save()
		return lawyer

class Lawyer(models.Model):
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	balance = models.DecimalField(max_digits=16, decimal_places=3, default=0)
	blacklist = models.BooleanField(default=False)
	score = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to='avatar.lawyer/', max_length=255, null=True)
	# TODO 注释下面两行，确保其他代码没有引用到它们
	# remarks = models.ManyToManyField(Client, through="Remark", through_fields=("lawyer","client"), related_name="c_l_remarks")
	# questions = models.ManyToManyField(Client, through="Question", through_fields=("lawyer","client"), related_name="c_l_questions")

	objects = LawyerManager()

	class Meta:
		verbose_name = u'律师'
		verbose_name_plural = u'律师'

	def __unicode__(self):
		return self.user.username

	@transaction.atomic
	def plus_score(self): 
		self.score+=1
		self.save()


class Remark(models.Model):
	lawyer = models.ForeignKey(Lawyer)
	client = models.ForeignKey(Client)
	grade = models.IntegerField(default=0)
	publish_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.grade)

class EnumActivityState(Enum):
	NEW = 0
	VIEWED = 1

class Activity(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255)
	state = models.IntegerField(default=EnumActivityState.NEW, choices=EnumActivityState.get_choices())
	publish_date = models.DateTimeField(auto_now=True, null=True)
