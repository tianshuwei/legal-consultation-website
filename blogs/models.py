# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User

class BlogCategory(models.Model):
	lawyer = models.ForeignKey("accounts.Lawyer")
	name = models.CharField(max_length=255, default='', unique=True)
	state = models.IntegerField(default=0) # 0=PUBLIC 1=PRIVATE -1=SYSTEM 

	def __unicode__(self):
		return self.name

	@transaction.atomic
	def remove(self):
		if self.state<0: return
		self.blogarticle_set.all().update(category=self.get_default())
		self.delete()

	def get_default(self):
		default_category, created=BlogCategory.objects.get_or_create(lawyer=self.lawyer,name=u"默认")
		if created: default_category.state=-1
		default_category.save()
		return default_category

class BlogArticleManager(models.Manager):
	use_for_related_fields = True
	def get_public_articles(self):
		return self.get_queryset().filter(category__isnull=False).order_by('-publish_date')

class BlogArticle(models.Model):
	author = models.ForeignKey("accounts.Lawyer", on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255, default='')
	publish_date = models.DateTimeField('date published', auto_now=True)
	category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
	tags = models.CharField(max_length=255, default='')
	text = models.TextField()

	objects = BlogArticleManager()

	def __unicode__(self):
		return self.title

	def remove(self):
		self.category=None
		self.save()

class BlogComment(models.Model):
	user = models.ForeignKey(User)
	publish_date = models.DateTimeField('date published', auto_now=True)
	article = models.ForeignKey(BlogArticle)
	text = models.TextField()

	def __unicode__(self):
		return self.text[:20]

class BlogSettings(models.Model):
	lawyer=models.OneToOneField("accounts.Lawyer")
	state=models.IntegerField(default=0)
	items_per_page=models.IntegerField(default=15)

	def __unicode__(self):
		return self.lawyer.user.username
