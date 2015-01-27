# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User

class BlogCategoryManager(models.Manager):
	use_for_related_fields = True

	def get_public_categories(self):
		return self.filter(state__lte=0).annotate(articles_count=models.Count('blogarticle')).order_by('name')

	def get_default_category(self, lawyer):
		default_category, created=BlogCategory.objects.get_or_create(lawyer=lawyer,name=u"默认")
		if created: 
			default_category.state=-1
			default_category.save()
		return default_category

class BlogCategory(models.Model):
	lawyer = models.ForeignKey("accounts.Lawyer")
	name = models.CharField(max_length=255, default='', unique=True)
	state = models.IntegerField(default=0) # 0=PUBLIC 1=PRIVATE -1=SYSTEM 

	objects = BlogCategoryManager()

	class Meta:
		verbose_name_plural = 'blog categories'

	def __unicode__(self):
		return self.name

	@transaction.atomic
	def remove(self):
		if self.state<0: return
		self.blogarticle_set.all().update(category=BlogCategory.objects.get_default_category(self.lawyer))
		self.delete()

	def get_recommended(self):
		return self.blogarticle_set.defer('text').order_by('-publish_date')[:6]

class BlogArticleManager(models.Manager):
	use_for_related_fields = True

	def get_public_articles(self):
		return self.filter(category__isnull=False).order_by('-publish_date')

	def get_public_articles_tagged(self, *taglist):
		return self.tagged(*taglist).filter(category__isnull=False).order_by('-publish_date')

	def get_tags(self):
		r=dict()
		for article in self.get_queryset().defer('text'):
			for tag in article.get_tags():
				if tag in r: r[tag]+=1
				else: r[tag]=1
		return [{'name': tag, 'count': count} for tag,count in ((t,r[t]) for t in r) if count]

	def tagged(self, *taglist):
		r=self.defer('text')
		for tag in taglist:
			r=r.filter(tags__regex=''.join([r'\m',tag,r'\M']))
		return r

	def tagged_any(self, *taglist):
		tags=''.join(['(','|'.join(taglist),')'])
		return self.defer('text').filter(tags__regex=''.join([r'\m',tags,r'\M']))

	def search(self, query):
		# TODO search
		return self.extra(where=["tags||' '||title @@ %s or text@@%s"], params=[query,query]).order_by('-publish_date')

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
