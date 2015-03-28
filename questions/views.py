# -*- coding: utf-8 -*-
from org.tools import *
from django.contrib.auth.models import User
from accounts.models import Lawyer, Client, Activity
from questions.models import Question, Question_text, EnumUser_flag

@login_required
def question_view(request, pk_question):
	question=get_object_or_404(Question, pk=pk_question)
	return response(request, 'questions/question.html',
		question=question,
		question_texts=Question_text.objects.filter(question_id=pk_question)
	)

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'lawyer', 'description']

@login_required
def new_question_view(request):
	if request.method=='POST':
		rec=recorded(request,'blogs:delete_article')
		try:
			with transaction.atomic():
				question=Question.objects.create(
					client=request.user.client,
					title=request.POST['title'],
					# lawyer=Lawyer.objects.get(id=request.POST['lawyer']),
					description=request.POST['description'],
				)
				question.save()
				request.user.client.minus_points()
		# TODO 律师可以为None，这种情况表示所有律师可以回答
		except ObjectDoesNotExist,e: 
			messages.error(request, u'问题创建失败')
			rec.error(u'{0} 创建问题失败，因为客户不存在'.format(request.user.username))
			handle_illegal_access(request)
		except: # Untestable!
			# TODO log trackback
			messages.error(request, u'问题创建失败')
			rec.error(u'{0} 创建问题失败'.format(request.user.username))
			handle_illegal_access(request)
		else:
			messages.success(request, u'问题创建成功')
			rec.success(u'{0} 创建问题 {1} 成功'.format(request.user.username, question.title))
			return redirect('questions:question',pk_question=question.id)
	else:
		return response(request, 'questions/new_question.html',
			question_create=QuestionForm())

@login_required
def new_question_text_view(request, pk_question):
	# TODO 加入容错
	q = get_object_or_404(Question, pk=pk_question)
	# TODO 封装下面语句，user_flag判断封装到models
	q_text = Question_text.objects.create(
		replier=request.user,
		text=request.POST['txt_question'], 
		user_flag=EnumUser_flag.ASK if get_role(request.user).is_client else EnumUser_flag.ANSWER, 
		question=q
	)
	q_text.save()
	Activity.objects.notify_new_reply(q.client.user, q_text)
	return redirect('questions:question', pk_question=q.id)

@login_required
def question_satisfied(request, pk_question):
	# TODO 加入容错
	qu = get_object_or_404(Question, pk=pk_question)
	qu.finish()
	la = get_object_or_404(Lawyer, pk=qu.lawyer_id)
	la.plus_score()
	return redirect('questions:question', pk_question=qu.id)

def index_view(request):
	return response(request, 'questions/index.html',
		latest_questions_list=Question.objects.order_by('-publish_date'),
		#TODO sort by the amount of question_text
		hot_question=Question.objects.order_by('-publish_date') )