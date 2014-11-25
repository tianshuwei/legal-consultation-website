from django.db import models

class BlogCategory(models.Model):
	user = models.ForeignKey("accounts.Lawyer")
	name = models.CharField(max_length=256, default='')

	def __unicode__(self):
		return self.name
		
class BlogArticle(models.Model):
	title = models.CharField(max_length=256, default='')
	publish_date = models.DateTimeField('date published', auto_now=True)
	category = models.ForeignKey(BlogCategory)
	tags = models.CharField(max_length=256, default='')
	text = models.TextField()

	def __unicode__(self):
		return self.title

class BlogComment(models.Model):
	user = models.ForeignKey("accounts.Lawyer")
	publish_date = models.DateTimeField('date published', auto_now=True)
	article = models.ForeignKey(BlogArticle)
	text = models.TextField()

	def __unicode__(self):
		return self.text[:20]
