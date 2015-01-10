# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render
from settings import DEBUG
from index.models import TransactionRecord
from datetime import datetime
import random

# def debugonly(func):
# 	return func if DEBUG else lambda:None

def transacserial(transaction_name):
	return ''.join([
		transaction_name[:2].upper(),
		datetime.now().strftime("%Y%m%d%H%M%S"),
		''.join(random.choice('QWERTYUIOPASDFGHJKLZXCVBNMZY') for i in xrange(4))
	])

TRANSACSERIAL='transacserial'
def recorded(request, transaction_name):
	if request.method=='POST' and TRANSACSERIAL in request.POST:
		return TransactionRecord.objects.create(
			title=transaction_name.lower(),
			serial=request.POST['transacserial'],
			result='unknown'
		)
	else: 
		return lambda msg: msg

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

def url_of(url_ref, **kwargs):
	return reverse(url_ref, kwargs = kwargs)

def response(request, template_name, **context):
	"""
	常规HTTP响应

		request        被响应HTTP请求
		template_name  模板
		context        模板上下文变量
	"""
	return HttpResponse(loader.get_template(template_name).render(RequestContext(request, dict(context, 
		is_lawyer = Lazy(lambda: get_role(request.user).is_lawyer),
		is_client = Lazy(lambda: get_role(request.user).is_client),
	))))

import json
def response_jquery(o):
	"""
	json格式序列化python对象作为HTTP响应

		o              简单的python对象
	"""
	return HttpResponse(json.dumps(o), content_type="application/json")

JSSUBMITTEDMARK='jssubmittedmark'
def response_auto(request, o, url_ref, **kwargs):
	"""
	根据请求形式自动选择redirect或response_jquery来响应。适合两种情况都要响应的view。

	若请求通过普通表单提交，则调用redirect(url_ref, **kwargs)；
	若请求通过$submit提交，则调用response_jquery(o)。

		o 				response_jquery的参数
		url_ref 		redirect的参数
		**kwargs 		redirect的参数
	"""
	return response_jquery(o) if JSSUBMITTEDMARK in request.POST and request.POST[JSSUBMITTEDMARK]=='$submit 2014' else redirect(url_ref, **kwargs)

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
	try: current=int(pagenumf())
	except: current=1
	paginator = Paginator(dataset, items_per_page)
	if current>paginator.num_pages: current=paginator.num_pages
	if current<1: current=1
	page=paginator.page(current)
	page.page_range=sorted(set(filter(lambda i:i in paginator.page_range, range(current-2,current+6)+[current+10,(1+current)/2,(current+paginator.count)/2])))
	return page

from accounts.models import Lawyer, Client
def get_role(user):
	def foo(user):
		try: return user.lawyer
		except:
			try: return user.client
			except: return user
	u = foo(user)
	u.is_lawyer = type(u) is Lawyer
	u.is_client = type(u) is Client
	return u

# def message(request,msg=None):
# 	if msg: request.session['result_text'] = msg
# 	else: del request.session['result_text']
from django.contrib import messages
__messages_override=['debug','error','info','success','warning']
__messages={funcname:getattr(messages,funcname) for funcname in __messages_override}
for funcname in __messages_override:
	def foo(request,message,unconditional=False):
		if unconditional or JSSUBMITTEDMARK not in request.POST:
			return __messages[funcname](request,message)
	setattr(messages,funcname,foo)

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django import forms
import traceback
