# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from org.types import Enum

class EnumSmartContractCategoryState(Enum):
	PUBLIC = 0

class SmartContractCategory(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(u'合同分类名称', max_length=120)
	state = models.IntegerField(u'合同分类状态', default=EnumSmartContractCategoryState.PUBLIC, choices=EnumSmartContractCategoryState.get_choices())

	class Meta:
		verbose_name = u'合同分类'
		verbose_name_plural = u'合同分类'

	def __unicode__(self):
		return self.name

class EnumSmartContractState(Enum):
	DEFAULT = 0

class SmartContract(models.Model):
	category = models.ForeignKey(SmartContractCategory)
	name = models.CharField(u'合同名称', max_length=255)
	publish_date = models.DateTimeField(u'创建日期', default=datetime.now)
	state = models.IntegerField(u'合同状态', default=EnumSmartContractState.DEFAULT, choices=EnumSmartContractState.get_choices())
	template = models.FileField(u'DOCX模板', upload_to='smart/', max_length=255, null=True, blank=True)
	config = models.TextField(u'合同表单设计', blank=True)

	class Meta:
		verbose_name = u'合同模板'
		verbose_name_plural = u'合同模板'

	def __unicode__(self):
		return self.name

# class EnumSmartContractTemplateState(Enum):
# 	DEFAULT = 0

# class SmartContractTemplate(models.Model):
# 	contract = models.ForeignKey(SmartContract)
# 	template_type = models.CharField(max_length=32, default='')
# 	text = models.TextField()
# 	state = models.IntegerField(default=EnumSmartContractTemplateState.DEFAULT)

# 	def __unicode__(self):
# 		return self.template_type

# class SmartContractStep(models.Model):
# 	contract = models.ForeignKey(SmartContract)
# 	name = models.CharField(max_length=30, default='')
# 	next_name = models.CharField(max_length=30, default='')

# 	def __unicode__(self):
# 		return self.name

# class SmartContractVar(models.Model):
# 	step = models.ForeignKey(SmartContractStep)
# 	widget = models.IntegerField(default=0)
# 	extra = models.TextField()
# 	name = models.CharField(max_length=30, default='')
# 	label = models.CharField(max_length=255, default='')
# 	help_text = models.CharField(max_length=255, default='')
# 	next_name = models.CharField(max_length=30, default='')

# 	def __unicode__(self):
# 		return self.name

class SmartContractInstance(models.Model):
	contract = models.ForeignKey(SmartContract)
	user = models.ForeignKey(User)
	data = models.TextField(u'合同数据', blank=True)

	class Meta:
		verbose_name = u'合同实例'
		verbose_name_plural = u'合同实例'

	def __unicode__(self):
		return u"%s %s" % (self.user.username, self.contract.name)

