from django.db import models
from django.contrib.auth.models import User

class BlogCategory(models.Model):
	lawyer = models.ForeignKey("accounts.Lawyer")
	name = models.CharField(max_length=255, default='', unique=True)

	def __unicode__(self):
		return self.name

class BlogArticle(models.Model):
    author = models.ForeignKey("accounts.Lawyer")
    title = models.CharField(max_length=255, default='')
    publish_date = models.DateTimeField('date published', auto_now=True)
    category = models.ForeignKey(BlogCategory)
    tags = models.CharField(max_length=255, default='')
    text = models.TextField()

    def __unicode__(self):
        return self.title

class BlogComment(models.Model):
	user = models.ForeignKey(User)
	publish_date = models.DateTimeField('date published', auto_now=True)
	article = models.ForeignKey(BlogArticle)
	text = models.TextField()

	def __unicode__(self):
		return self.text[:20]

class BlogSettings(models.Model):
	lawyer=models.ForeignKey("accounts.Lawyer")
	state=models.IntegerField(default=0)
	items_per_page=models.IntegerField(default=0)

	def __unicode__(self):
		return self.lawyer.user.username
