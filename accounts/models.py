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
	balance = models.DecimalField(max_digits=16, decimal_places=3)
	points = models.IntegerField()

	def __unicode__(self):
		return self.user.username
	
class Lawyer(models.Model):
	user = models.OneToOneField(User)
	balance = models.DecimalField(max_digits=16, decimal_places=3)
	blacklist = models.BooleanField(default=False)
	score = models.IntegerField()
	blog = models.URLField(max_length=512)

	def __unicode__(self):
		return self.user.username
