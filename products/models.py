from django.db import models

class Product(models.Model):
	name = models.CharField(max_length=256,default='')
	publish_date = models.DateTimeField('date published',auto_now=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=16, decimal_places=3,default=0)

	def __unicode__(self):
		return self.name
