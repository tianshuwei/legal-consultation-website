# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models, transaction
from django.db.models import Q
from django.contrib.auth.models import User
from org.settings import DATABASES
from org.dbtools import rawsql
from org.types import Enum, CustomException

POSTGRESQL = 'postgresql' in DATABASES['default']['ENGINE']
EN_FULLTEXTSEARCH = False

class BlogCategoryManager(models.Manager):
	use_for_related_fields = True

	def get_public_categories(self):
		return self.filter(state__lte=EnumBlogCategoryState.PUBLIC).annotate(articles_count=models.Count('blogarticle')).order_by('name')

	def get_default_category(self, lawyer):
		r, created=BlogCategory.objects.get_or_create(lawyer=lawyer,name=u"默认")
		if created: 
			r.state=EnumBlogCategoryState.SYSTEM
			r.save()
		return r

class EnumBlogCategoryState(Enum):
	PUBLIC = 0
	PRIVATE = 1
	SYSTEM = -1

class BlogCategory(models.Model):
	lawyer = models.ForeignKey("accounts.Lawyer")
	name = models.CharField(max_length=255, default='', unique=True)
	state = models.IntegerField(default=EnumBlogCategoryState.PUBLIC)

	objects = BlogCategoryManager()

	class Meta:
		verbose_name = u'博客分类'
		verbose_name_plural = u'博客分类'

	def __unicode__(self):
		return self.name

	@transaction.atomic
	def remove(self):
		if self.state==EnumBlogCategoryState.SYSTEM: return
		self.blogarticle_set.all().update(category=BlogCategory.objects.get_default_category(self.lawyer))
		self.delete()

	def get_recommended(self):
		return self.blogarticle_set.defer('text').order_by('-publish_date')[:6]

class BlogArticleManager(models.Manager):
	use_for_related_fields = True

	def get_public_articles(self):
		return self.filter(category__isnull=False).order_by('-publish_date')

	def get_favourite_articles(self):
		return self.filter(category__isnull=False).order_by('-clicks')[:6]

	def get_archived_articles(self, year, month):
		return self.filter(publish_date__year=year, publish_date__month=month).order_by('-publish_date')

	def get_archives(self, pk_lawyer=None):
		def compatible_way(dataset):
			z = [datetime(article.publish_date.year,article.publish_date.month,1) for article in dataset]
			return [{'publish_date': d, 'count': z.count(d)} for d in reversed(sorted(set(z)))]
		if pk_lawyer==None:
			return compatible_way(self.defer('text'))
		elif POSTGRESQL:
			return rawsql(['publish_date','count'],
			"""SELECT date_trunc('month',publish_date), COUNT(*) 
				FROM blogs_blogarticle 
				WHERE author_id = %s
				GROUP BY date_trunc('month',publish_date)
				ORDER BY date_trunc('month',publish_date) DESC;""", 
			params=[pk_lawyer])
		else:
			return compatible_way(self.defer('text').filter(author__id=pk_lawyer))

	def get_public_articles_tagged(self, *taglist):
		return self.tagged(*taglist).filter(category__isnull=False).order_by('-publish_date')

	def get_tags(self, pk_lawyer=None):
		def compatible_way(dataset):
			z = [tag for article in dataset for tag in article.get_tags()]
			return [{'name': tag, 'count': z.count(tag)} for tag in sorted(set(z))]
		if pk_lawyer==None:
			return compatible_way(self.defer('text'))
		elif POSTGRESQL:
			return rawsql(['name','count'],
			"""SELECT regexp_split_to_table(tags::text, ', *'::text), COUNT(*)
				FROM blogs_blogarticle
				WHERE author_id = %s
				GROUP BY regexp_split_to_table(tags::text, ', *'::text)
				ORDER BY regexp_split_to_table(tags::text, ', *'::text);""",
			params=[pk_lawyer])
		else:
			return compatible_way(self.defer('text').filter(author__id=pk_lawyer))

	def tagged_one(self, tag):
		if POSTGRESQL:
			# return self.filter(tags__regex=''.join([r'\m',tag,r'\M'])) # word boundary used in psql
			return self.extra(where=["regexp_split_to_array(tags,',\x20*')@>array[%s]"],params=[tag])
		else:
			return self.filter(tags__regex=''.join([r'[[:<:]]',tag,r'[[:>:]]'])) # word boundary used in psql

	def tagged(self, *taglist):
		if POSTGRESQL:
			return self.extra(where=["regexp_split_to_array(tags,',\x20*')@>regexp_split_to_array(%s, ',')"],params=[','.join(taglist)]) if len(taglist)>1 else self.tagged_one(taglist[0])
		else:
			r=self.defer('text')
			for tag in taglist:
				r=r.filter(tags__regex=''.join([r'[[:<:]]',tag,r'[[:>:]]']))
			return r

	def tagged_any(self, *taglist):
		if POSTGRESQL:
			return self.extra(where=["regexp_split_to_array(tags,',\x20*')&&regexp_split_to_array(%s, ',')"],params=[','.join(taglist)]) if len(taglist)>1 else self.tagged_one(taglist[0])
		else:
			tags=''.join(['(','|'.join(taglist),')'])
			return self.defer('text').filter(tags__regex=''.join([r'[[:<:]]',tags,r'[[:>:]]']))

	def search(self, query):
		if EN_FULLTEXTSEARCH and POSTGRESQL:
			return self.extra(where=["tags||' '||title @@ %s or text@@%s"], params=[query,query]).order_by('-publish_date')
		else:
			return self.filter(Q(tags__contains=query)|Q(title__contains=query)|Q(text__contains=query)).order_by('-publish_date')

class BlogArticle(models.Model):
	author = models.ForeignKey("accounts.Lawyer", on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255, default='')
	modify_date = models.DateTimeField(auto_now=True, null=True)
	publish_date = models.DateTimeField()
	clicks = models.IntegerField(default=0)
	category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
	tags = models.CharField(max_length=255, default='')
	text = models.TextField()

	objects = BlogArticleManager()

	class Meta:
		verbose_name = u'博客文章'
		verbose_name_plural = u'博客文章'

	def __unicode__(self):
		return self.title

	def get_tags(self):
		z=[i.strip() for i in self.tags.split(',')]
		return list() if len(z)==1 and z[0]=='' else z

	def get_tags_along_with_recommended(self):
		return [{
			'name':tag, 
			'recommended': self.author.blogarticle_set.tagged(tag).filter(category__isnull=False).order_by('-publish_date')[:6]
		} for tag in self.get_tags()]

	def get_other_related_articles(self):
		return BlogArticle.objects.tagged_any(*self.get_tags()).filter(category__isnull=False).order_by('-publish_date')[:6]

	def remove(self):
		self.category=None
		self.save()

	def touch(self):
		self.clicks+=1
		self.save()

class BlogCommentManager(models.Manager):
	use_for_related_fields = True

	def get_recent_comments(self, lawyer):
		return self.filter(article__author=lawyer).order_by('-publish_date')[:6]

class BlogComment(models.Model):
	user = models.ForeignKey(User)
	publish_date = models.DateTimeField('date published', auto_now=True)
	article = models.ForeignKey(BlogArticle)
	text = models.TextField()

	objects=BlogCommentManager()

	def __unicode__(self):
		return self.text[:20]

class BlogSettingsManager(models.Manager):
	def get_blogsettings(self, lawyer):
		from accounts.models import Lawyer
		r, created=self.get_or_create(lawyer=lawyer)
		if r.state==EnumBlogSettingsState.DISABLE: raise CustomException('Blog disabled')
		return r

class EnumBlogSettingsState(Enum):
	PUBLIC = 0
	DISABLE = 1

class BlogSettings(models.Model):
	lawyer = models.OneToOneField("accounts.Lawyer")
	state = models.IntegerField(default=EnumBlogSettingsState.PUBLIC)
	items_per_page = models.IntegerField(default=15)

	objects = BlogSettingsManager()

	def __unicode__(self):
		return self.lawyer.user.username
