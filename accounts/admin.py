# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import Client, Lawyer, Remark, Question, Question_text

class ClientOrLawyerFilter(admin.SimpleListFilter):
	title = 'client or lawyer'
	parameter_name = 'CorL'

	def lookups(self, request, model_admin):
		return (
			('clients','Only clients'),
			('lawyers','Only lawyers'),
		)

	def queryset(self, request, queryset):
		if self.value()=='clients':
			return queryset.select_related('client').filter(client__isnull=False)

		if self.value()=='lawyers':
			return queryset.select_related('lawyer').filter(lawyer__isnull=False)

class ClientInline(admin.StackedInline):
	model = Client
	# can_delete = False
	verbose_name_plural = u'客户扩展属性（仅限客户）'

class LawyerInline(admin.StackedInline):
	model = Lawyer
	# can_delete = False
	verbose_name_plural = u'律师扩展属性（仅限律师）'

class MyUserAdmin(UserAdmin):
	inlines = (ClientInline, LawyerInline)
	list_filter = UserAdmin.list_filter + (ClientOrLawyerFilter,)

class Question_textInline(admin.TabularInline):
	model = Question_text
	verbose_name_plural = 'question_texts'

class QuestionAdmin(admin.ModelAdmin):
	inlines = [Question_textInline]

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Remark)
