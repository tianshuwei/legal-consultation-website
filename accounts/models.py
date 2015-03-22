# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from org.types import Enum
from org.settings import DATABASES
from org.dbtools import rawsql

POSTGRESQL = 'postgresql' in DATABASES['default']['ENGINE']

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

	@transaction.atomic
	def add_balance(self,count): 
		self.balance+=count
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

class ActivityManager(models.Manager):
	use_for_related_fields = True

	@transaction.atomic
	def mark_viewed(self):
		self.update(state=EnumActivityState.VIEWED)

	def count_new_activities(self, pk_user):
		def compatible_way(dataset):
			z = [tag for article in dataset for tag in article.get_tags()]
			return [{'name': tag, 'count': z.count(tag)} for tag in sorted(set(z))]
		if POSTGRESQL:
			return rawsql(['name','count'],
			"""SELECT regexp_split_to_table(tags::text, ', *'::text), COUNT(*)
				FROM accounts_activity
				WHERE state = %s AND user_id = %s
				GROUP BY regexp_split_to_table(tags::text, ', *'::text)
				ORDER BY regexp_split_to_table(tags::text, ', *'::text);""",
			params=[EnumActivityState.NEW, pk_user])
		else:
			return compatible_way(self.filter(state=EnumActivityState.NEW, user__id=pk_user))

	@transaction.atomic
	def notify_new_reply(self, user, reply):
		r = self.create(
			user=user, 
			title=u'{0} 回复了您提出的问题 {1}'.format(
				reply.replier.username, 
				reply.question.title
			),
			tags='question_new_reply'
		)
		r.save()

	@transaction.atomic
	def notify_new_blog_comment(self, user, comment):
		r = self.create(
			user=user, 
			title=u'{0} 评论了您的博客文章 {1}'.format(
				comment.user.username, 
				comment.article.title
			),
			tags='blog_comment'
		)
		r.save()

	@transaction.atomic
	def notify_order_update(self, user, order):
		from products.models import EnumOrderState
		translation = {
			EnumOrderState.UNPAID: u'创建',
			EnumOrderState.IN_BUSINESS: u'支付',
			EnumOrderState.FINISHED: u'完成',
			EnumOrderState.CANCELLED: u'取消',
		}
		r = self.create(
			user=user, 
			title=u'您的订单 {0} 已{1}'.format(
				order.serial, 
				translation[order.state]
			),
			tags='order_update'
		)
		r.save()

class Activity(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255)
	tags = models.CharField(max_length=255, blank=True, default='')
	state = models.IntegerField(default=EnumActivityState.NEW, choices=EnumActivityState.get_choices())
	publish_date = models.DateTimeField(auto_now=True, null=True)

	objects = ActivityManager()

	@transaction.atomic
	def mark_viewed(self):
		self.state=EnumActivityState.VIEWED
		self.save()
