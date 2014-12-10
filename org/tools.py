# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render

# def message(request,msg=None):
# 	if msg: request.session['result_text'] = msg
# 	else: del request.session['result_text']

class Lazy(object):
	def __init__(self, f):
		super(Lazy, self).__init__()
		self.f, self.v, self.a = f, None, False

	def __call__(self):
		if not self.a: self.v, self.a = self.f(), True
		return self.v

def redirect(url_ref, **kwargs):
	"""
	HTTP重定向

		url_ref       url引用名
		kwargs        url中的命名参数
	"""
	return HttpResponseRedirect(reverse(url_ref, kwargs = kwargs))

def response(request, template_name, **context):
	"""
	常规HTTP响应

		request        被响应HTTP请求
		template_name  模板
		context        模板上下文变量
	"""
	return HttpResponse(loader.get_template(template_name).render(RequestContext(request, dict(context, 
		is_lawyer = Lazy(lambda: is_lawyer(request.user)),
		is_client = Lazy(lambda: is_client(request.user)),
	))))

import json
def response_jquery(o):
	"""
	json格式序列化python对象作为HTTP响应

		o              简单的python对象
	"""
	return HttpResponse(json.dumps(o), content_type="application/json")

def checkf(exp, default=None):
	"""
	求lambda表达式的值，异常返回default（默认为None）

		exp            一个无参lambda表达式
		default        异常返回默认值
	""" 
	try: return exp()
	except: return default

def paginated(pagenumf, items_per_page, dataset):
	"""
	结果集分页

		pagenumf       当前页码的lambda表达式
		items_per_page 每页项目数
		dataset        原结果集
	""" 
	paginator = Paginator(dataset, items_per_page)
	try: return paginator.page(pagenumf())
	except PageNotAnInteger: return paginator.page(1)
	except EmptyPage: return paginator.page(paginator.num_pages)

from accounts.models import Lawyer, Client

def get_role(user):
	try:return user.lawyer
	except Lawyer.DoesNotExist, e:
		try: return user.client
		except:return user

is_client = lambda user: type(get_role(user)) is Client
is_lawyer = lambda user: type(get_role(user)) is Lawyer

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django import forms

