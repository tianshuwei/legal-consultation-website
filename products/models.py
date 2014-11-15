from django.db import models

class Product(models.Model):
	name = models.CharField(max_length=256)
	publish_date = models.DateTimeField('date published')

	def __unicode__(self):
		return self.name
