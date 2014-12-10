# -*- coding: utf-8 -*-
from org.tools import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from accounts.models import Lawyer, Client

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
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(next_url)
		else: return HttpResponseRedirect(next_url)
	else:  return response(request, 'accounts/login.html')

def logout_view(request):
	logout(request)
	return redirect('index:index')

def register_view(request, role):
	if request.method=='POST':
		user=User.objects.create_user(request.POST['username'], 
			password=request.POST['password'],
			email=request.POST['email'],
			last_name = request.POST['last_name'],
			first_name = request.POST['first_name'],
		)
		user.save()
		if role=='client': Client.objects.create(user=user).save()
		elif role=='lawyer': Lawyer.objects.create(user=user).save()
		return redirect('accounts:login')
	else: return response(request, 'accounts/register.html', register_form=RegisterForm())

def lawyerlist_view(request):
	return response(request, 'accounts/lawyerlist.html',
		lawyers=Lawyer.objects.all())

@login_required
def usercenter_view(request):
	user = get_role(request.user)
	if type(user) is Lawyer: return response(request, 'accounts/lawyercenter.html')
	elif type(user) is Client: return response(request, 'accounts/usercenter.html')

@login_required
def profile_view(request):
	user = get_role(request.user)
	if type(user) is Lawyer: return response(request, 'accounts/profile_lawyer.html')
	elif type(user) is Client: return response(request, 'accounts/profile_client.html')
	else: return response(request, 'accounts/profile_default.html')

@login_required
def question_view(request, pk_question):
	raise Http404

@login_required
def order_detail_view(request, pk_order):
	raise Http404

@login_required
def balance_view(request):
	raise Http404

def remark_view(request, pk_lawyer):
	raise Http404

def new_question_view(request):
	raise Http404
