from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import Client, Lawyer, Remark, Question, Question_text

class ClientInline(admin.StackedInline):
	model = Client
	# can_delete = False
	verbose_name_plural = 'client'

class LawyerInline(admin.StackedInline):
	model = Lawyer
	# can_delete = False
	verbose_name_plural = 'lawyer'

class UserAdmin(UserAdmin):
	inlines = (ClientInline, LawyerInline)

class Question_textInline(admin.TabularInline):
	model = Question_text
	verbose_name_plural = 'question_texts'

class QuestionAdmin(admin.ModelAdmin):
	inlines = [Question_textInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Remark)
