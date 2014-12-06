from django.db import models
from django.contrib.auth.models import User

"""
Fields in User
	username
	password
	email
	first_name
	last_name
"""

class Client(models.Model):
	user = models.OneToOneField(User)
	balance = models.DecimalField(max_digits=16, decimal_places=3,default=0)
	points = models.IntegerField(default=0)
	#comments = models.ManyToManyField("products.Product", through="products.Comment", through_fields=("client","product"), related_name="c_p_comments")

	def __unicode__(self):
		return self.user.username

class Lawyer(models.Model):
	user = models.OneToOneField(User)
	balance = models.DecimalField(max_digits=16, decimal_places=3,default=0)
	blacklist = models.BooleanField(default=False)
	score = models.IntegerField(default=0)
	#blog = models.URLField(max_length=512)
	remarks = models.ManyToManyField(Client, through="Remark", through_fields=("lawyer","client"), related_name="c_l_remarks")
	questions = models.ManyToManyField(Client, through="Question", through_fields=("lawyer","client"), related_name="c_l_questions")

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

