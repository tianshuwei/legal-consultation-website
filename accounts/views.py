# -*- coding: utf-8 -*-
from org.tools import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from accounts.models import Lawyer, Client, Remark, Question, Question_text
from products.models import Order

class RegisterForm(forms.Form):
	username = forms.CharField(label="账户",max_length=254)
	last_name = forms.CharField(label="姓",max_length=20)
	first_name = forms.CharField(label="名",max_length=20)
	email = forms.EmailField(label="邮箱")
	password = forms.CharField(label="密码", widget=forms.PasswordInput)
	password_confirm = forms.CharField(label="密码确认", widget=forms.PasswordInput)

def login_view(request):
	if request.method=='POST':
		username,password = request.POST['username'],request.POST['password']
		next_url = request.GET['next'] if 'next' in request.GET else reverse('index:index')
		user = authenticate(username=username, password=password)
		rec=recorded(request,'login')
		if user is not None:
			login(request, user)
			rec.success(u'{0}登入成功'.format(username))
			return HttpResponseRedirect(next_url)
		else: 
			rec.error(u'{0}登入失败'.format(username))
			return HttpResponseRedirect(next_url)
	else:  return response(request, 'accounts/login.html')

def logout_view(request):
	logout(request)
	return redirect('index:index')

def register_view(request, role):
	if request.method=='POST':
		try:
			username,profile=request.POST['username'],dict(
				password=request.POST['password'],
				email=request.POST['email'],
				last_name = request.POST['last_name'],
				first_name = request.POST['first_name'],
			)
			if role=='client': 
				Client.objects.register(username,**profile)
			elif role=='lawyer': 
				Lawyer.objects.register(username,**profile)
		except: messages.success(request, u'注册失败')
		else: messages.success(request, u'注册成功')
		return redirect('accounts:login')
	else: return response(request, 'accounts/register.html', register_form=RegisterForm())

def lawyerlist_view(request):
	return response(request, 'accounts/lawyerlist.html',
		lawyers=Lawyer.objects.all())

@login_required
def usercenter_view(request):
	u = get_role(request.user)
	return response(request, 'accounts/usercenter.html',
		orders=paginated(lambda: request.GET.get('po'), 10, 
			u.order_set.order_by('-publish_date')),
		questions=paginated(lambda: request.GET.get('pq'), 10, 
			u.question_set.order_by('-publish_date')))

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['last_name', 'first_name', 'email']
		labels = {'last_name':u'姓', 'first_name':u'名', 'email':u'邮箱'}

@login_required
def profile_self_view(request):
	if request.method=='POST':
		form=ProfileEditForm(request.POST, instance=request.user)
		form.save()
		messages.success(request, u'个人资料编辑成功')
		return redirect('accounts:profile_self')
	else: return response(request, 'accounts/profile.html', 
		role=get_role(request.user), 
		is_master=True,
		profile_edit=ProfileEditForm(instance=request.user))

def profile_view(request, role, pk):
	if role=='c': u = get_object_or_404(Client,pk=pk)
	elif role=='l': u = get_object_or_404(Lawyer,pk=pk)
	else: raise Http404
	return response(request, 'accounts/profile.html', role=u)

@login_required
def question_view(request, pk_question):
	question=get_object_or_404(Question, pk=pk_question)
	return response(request, 'accounts/question.html',
		question=question,
		question_texts=Question_text.objects.filter(question_id=pk_question)
	)


@login_required
def order_detail_view(request, pk_order):
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		try:
			if request.user.client==order.client:
				order.text=request.POST['text']
				order.save()
			else: raise Exception
		except: messages.error(request, u'备注修改失败')
		else: messages.success(request, u'备注修改成功')
		return redirect('accounts:order_detail', pk_order=pk_order)
	else: return response(request, 'accounts/order_detail.html', order=order)

@login_required
def order_delete_view(request, pk_order): # TODO use post in template
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		try:
			if request.user.client==order.client: order.delete()
			else: raise Exception			
		except: messages.error(request, u'取消订单失败')	
		else: messages.success(request, u'取消订单成功')
		return redirect('accounts:usercenter')
	else: raise Http404

from decimal import Decimal
@login_required
def balance_view(request):
	u = get_role(request.user)
	if request.method=='POST':
		try:
			u.balance+=Decimal(request.POST['amount'])
			u.save()
			messages.success(request, u'充值成功')
		except: messages.error(request, u'充值失败')
		return redirect('accounts:balance')
	else: return response(request, 'accounts/balance.html', role=u)

class RemarkForm(forms.ModelForm):
	class Meta:
		model = Remark
		fields = ['grade']
		labels = { 'grade' : u'评分' }

@login_required
def remark_view(request, pk_lawyer):
	lawyer = get_object_or_404(Lawyer, pk=pk_lawyer)
	remark, created = Remark.objects.get_or_create(client=request.user.client,lawyer=lawyer)
	if request.method=='POST':
		try:
			remark.grade=int(request.POST['grade'])
			remark.save()
			messages.success(request, u'评价成功')
		except: messages.error(request, u'评价失败')
		return redirect('accounts:remark', pk_lawyer=pk_lawyer)
	else: 
		return response(request, 'accounts/remark.html', 
			remark=remark,
			remark_form=RemarkForm(instance=remark), 
		)

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'lawyer', 'description']
		labels = {
			'title' : u'标题',
			'lawyer' : u'律师',
			'description' : u'描述',
		}

@login_required
def new_question_view(request):
	if request.method=='POST':
		try:
			qu=Question.objects.create(
				client=request.user.client,
				title=request.POST['title'],
				lawyer=Lawyer.objects.get(id=request.POST['lawyer']),
				description=request.POST['description']
			)
			qu.save()
		except ObjectDoesNotExist,e: raise Http404
		except : messages.error(request, u'问题创建失败')
		else: messages.success(request, u'问题创建成功')
		return redirect('accounts:question',pk_question=qu.id)
	else: 
		return response(request, 'accounts/new_question.html', 
			question_create=QuestionForm())

@login_required
def new_question_text_view(request, pk_question):
	q = get_object_or_404(Question, pk=pk_question)
	q_text = Question_text.objects.create(text=request.POST['txt_question'], user_flag=1 if get_role(request.user).is_client else 0, question=q)
	q_text.save()
	return redirect('accounts:question', pk_question=q.id)
