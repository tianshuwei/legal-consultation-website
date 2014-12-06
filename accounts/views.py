from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label="Username",max_length=254)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)

class RegisterForm(forms.Form):
	username = forms.CharField(label="Username",max_length=254)
	first_name = forms.CharField(label="First Name",max_length=20)
	last_name = forms.CharField(label="Last Name",max_length=20)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	password_confirm = forms.CharField(label="Password Confirm", widget=forms.PasswordInput)

def login_view(request):
	if request.method=='POST':
		username,password = request.POST['username'],request.POST['password']
		next_url=request.POST['next']
		user = authenticate(username=username, password=password)
		if user is not None:
			print 'Login ok'
			login(request, user)
			#if(request=="new_order") return HttpResponseRedirect(reverse('products:detail'))
			return HttpResponseRedirect(reverse('index:index'))
		else:
			print 'Login err'
			return HttpResponseRedirect(reverse('index:index'))

	else:
		login_form=LoginForm()
		template = loader.get_template('accounts/login.html')
		context = RequestContext(request, {
			'login_form':login_form,
			'next_url':request.GET['next']
		})
		return HttpResponse(template.render(context))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index:index'))

def register_view(request):
	if request.method=='POST':
		User.objects.create_user(request.POST['username'], password=request.POST['password'])
		return HttpResponseRedirect(reverse('accounts:login'))
	else:
		register_form=RegisterForm()
		template = loader.get_template('accounts/register.html')
		context = RequestContext(request, {
			'register_form':register_form
		})
		return HttpResponse(template.render(context))

# def login(request):
# 	latest_products_list = Product.objects.order_by('-publish_date')[:5]
# 	template = loader.get_template('index/index.html')
# 	context = RequestContext(request, {
# 		'latest_products_list': latest_products_list,
# 	})
# 	return HttpResponse(template.render(context))

def lawyerlist_view(request):
    raise Http404

def usercenter_view(request):
    raise Http404

def lawyercenter_view(request):
    raise Http404

def profile_view(request):
    raise Http404

def question_view(request, pk):
    raise Http404

def order_detail_view(request, pk):
    raise Http404

def balance_view(request):
    raise Http404

def remark_view(request, pk):
    raise Http404

def new_question_view(request):
    raise Http404
