from django.contrib import admin

from questions.models import Question, Question_text

class Question_textInline(admin.TabularInline):
	model = Question_text
	verbose_name_plural = 'question_texts'

class QuestionAdmin(admin.ModelAdmin):
	inlines = [Question_textInline]

admin.site.register(Question, QuestionAdmin)
