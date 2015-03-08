# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import Client, Lawyer, Remark, Question, Question_text
from blogs.models import BlogSettings

class ClientOrLawyerFilter(admin.SimpleListFilter):
	title = u'用户角色'
	parameter_name = 'CorL'

	def lookups(self, request, model_admin):
		return (
			('clients',u'仅客户'),
			('lawyers',u'仅律师'),
		)

	def queryset(self, request, queryset):
		if self.value()=='clients':
			return queryset.select_related('client').filter(client__isnull=False)

		if self.value()=='lawyers':
			return queryset.select_related('lawyer').filter(lawyer__isnull=False)

class LawyerInline(admin.StackedInline):
	model = BlogSettings
	can_delete = False
	verbose_name_plural = u'律师博客设置'

class MyUserAdmin(UserAdmin):
	list_filter = UserAdmin.list_filter + (ClientOrLawyerFilter,)

class LawyerAdmin(admin.ModelAdmin):
	inlines = (LawyerInline,)

class Question_textInline(admin.TabularInline):
	model = Question_text
	verbose_name_plural = 'question_texts'

class QuestionAdmin(admin.ModelAdmin):
	inlines = [Question_textInline]

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Remark)
admin.site.register(Lawyer, LawyerAdmin)
admin.site.register(Client)
