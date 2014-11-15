from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(label="Username",max_length=254)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)

def login_view(request):
	if request.method=='POST':
		username,password = request.POST['username'],request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/index')
		else:
			return HttpResponseRedirect('/index')

	else:
		login_form=LoginForm()
		template = loader.get_template('accounts/login.html')
		context = RequestContext(request, {
			'login_form':login_form
		})
		return HttpResponse(template.render(context))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/index')

def register_view(request):
	pass

# def login(request):
# 	latest_products_list = Product.objects.order_by('-publish_date')[:5]
# 	template = loader.get_template('index/index.html')
# 	context = RequestContext(request, {
# 		'latest_products_list': latest_products_list,
# 	})
# 	return HttpResponse(template.render(context))

