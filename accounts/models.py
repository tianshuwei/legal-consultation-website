# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models, transaction
from django.contrib.auth.models import User
from org.types import Enum
from org.settings import POSTGRESQL
from org.dbtools import rawsql

class ClientManager(models.Manager):
	@transaction.atomic
	def register(self, username, **profile):
		user=User.objects.create_user(username,**profile)
		user.save()
		client=Client.objects.create(user=user)
		client.save()
		# from index.models import SiteActivity
		# SiteActivity.objects.notify_new_user(user)
		return client

	def get_latest_reg_user(self):
		return self.order_by('-register_date')[:4]

class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	balance = models.DecimalField(u'余额', max_digits=16, decimal_places=3, default=0)
	points = models.IntegerField(u'积分', default=0)
	avatar = models.ImageField(u'头像', upload_to='avatar.client/', max_length=255, null=True, blank=True)
	register_date = models.DateTimeField(u'注册日期', default=datetime.now)
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
		# from index.models import SiteActivity
		# SiteActivity.objects.notify_new_user(user)
		return lawyer

class Lawyer(models.Model):
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	balance = models.DecimalField(u'余额', max_digits=16, decimal_places=3, default=0)
	blacklist = models.BooleanField(u'加入黑名单', default=False)
	score = models.IntegerField(default=0)
	avatar = models.ImageField(u'头像', upload_to='avatar.lawyer/', max_length=255, null=True, blank=True)
	register_date = models.DateTimeField(u'注册日期', default=datetime.now)
	job_title = models.CharField(u'职称', max_length=25, blank=True)
	intro = models.TextField(u'个人介绍', blank=True)
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
	grade = models.IntegerField(u'评分', default=0)
	publish_date = models.DateTimeField(u'评分日期', auto_now=True)

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
	def notify_questions_new_question(self, question):
		r = self.create(
			user=question.client.user, 
			title=u'您提出了问题 {0}'.format(
				question.title
			),
			tags='question_new_question,questions,S'
		)
		r.save()

	@transaction.atomic
	def notify_questions_new_reply(self, user, reply):
		r = self.create(
			user=user, 
			title=u'{0} 回复了您提出的问题 {1}'.format(
				reply.replier.username, 
				reply.question.title
			),
			tags='question_new_reply,questions,S'
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
			tags='blog_comment,blogs,S'
		)
		r.save()

	@transaction.atomic
	def notify_new_blog_article(self, article):
		r = self.create(
			user=article.author.user, 
			title=u'您发表了博客文章 {0}'.format(
				article.title
			),
			tags='blog_article,blogs,S'
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
			tags='orders,S'
		)
		r.save()

	@transaction.atomic
	def profile_new_blog_comment(self, user, comment):
		r = self.create(
			user=user, 
			title=u'评论了博客文章 {0}'.format(
				comment.article.title
			),
			tags='blog_comment,blogs,C'
		)
		r.save()

	@transaction.atomic
	def profile_new_product_comment(self, user, product):
		r = self.create(
			user=user, 
			title=u'评论了产品 {0}'.format(
				product.name
			),
			tags='product_comment,products,C'
		)
		r.save()

	def tagged_one(self, tag):
		if POSTGRESQL:
			# return self.filter(tags__regex=''.join([r'\m',tag,r'\M'])) # word boundary used in psql
			return self.extra(where=["regexp_split_to_array(tags,',\x20*')@>array[%s]"],params=[tag])
		else:
			return self.filter(tags__regex=''.join([r'[[:<:]]',tag,r'[[:>:]]'])) # word boundary used in psql


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
