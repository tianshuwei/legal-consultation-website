from django.db import models
from django.contrib.auth.models import User

class SmartContractCategory(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=120, default='', unique=True)

	def __unicode__(self):
		return self.name

class SmartContract(models.Model):
	category = models.ForeignKey(SmartContractCategory)
	name = models.CharField(max_length=255, default='')
	publish_date = models.DateTimeField('date published', auto_now=True)
	state = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class SmartContractTemplate(models.Model):
	contract = models.ForeignKey(SmartContract)
	template_type = models.CharField(max_length=32, default='')
	text = models.TextField()
	state = models.IntegerField(default=0)

	def __unicode__(self):
		return self.template_type

class SmartContractStep(models.Model):
	contract = models.ForeignKey(SmartContract)
	name = models.CharField(max_length=30, default='')
	next_name = models.CharField(max_length=30, default='')

	def __unicode__(self):
		return self.name

class SmartContractVar(models.Model):
	step = models.ForeignKey(SmartContractStep)
	widget = models.IntegerField(default=0)
	extra = models.TextField()
	name = models.CharField(max_length=30, default='')
	label = models.CharField(max_length=255, default='')
	help_text = models.CharField(max_length=255, default='')
	next_name = models.CharField(max_length=30, default='')

	def __unicode__(self):
		return self.name

class SmartContractInstance(models.Model):
	contract = models.ForeignKey(SmartContract)
	data = models.TextField()


