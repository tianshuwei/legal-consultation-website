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
	"""
	事务序列号

		transaction_name 事务名称，可以任意取，建议与该事务对应的POST请求的URL的name相同。

	形式：事务名称开头两位字母+日期时间+四位随机字母
	用来唯一标识一个功能性事务，一方面功能测试框架可以根据事务日志跟踪一个操作的结果，
	方便测试断言，解除测试与UI耦合；另一方面事务日志可作为网站的日志。

	事务日志的关系模式定义在 index.models.TransactionRecord 类中。

	首先，在模板里面用自定义filter（参数就是是事务名称），把事务序列号以hidden类型
	input元素形式渲染进表单中：

	{{ "login"|transacserial }}

		渲染结果类似 <input name="transacserial" type="hidden" value="LO20150111004128XBLT">

	处理POST请求的时候定义一个记录，recorded函数定义在tools.py中，它从request里面
	读出事务序列号，创建新记录：

	rec=recorded(request,'login')

	处理成功后调用这个对象来记录事务：

	rec(u'{0}登入成功'.format(username))

	功能测试中可以从HTML文档中找到input元素，获得事务序列号。凭事务序列号调用
	数据库API读取测试结果进行断言。
	"""
	return ''.join([
		transaction_name[:2].upper(),
		datetime.now().strftime("%Y%m%d%H%M%S"),
		''.join(random.choice('QWERTYUIOPASDFGHJKLZXCVBNMZY') for i in xrange(4))
	])

TRANSACSERIAL='transacserial'
def recorded(request, transaction_name):
	"""
	创建事务记录对象，返回值一定是恒等函数（语法糖，方便重复利用实参）。

		transaction_name 事务名称

	如果请求包含事务序列号，则建立事务日志，跟踪这个事务。
	否则返回一个什么都不干的恒等函数。
	"""
	rec = TransactionRecord.objects.create(
		title=transaction_name.lower(),
		serial=request.POST['transacserial'],
		result='unknown'
	) if request.method=='POST' and TRANSACSERIAL in request.POST else lambda msg: msg
	rec.save()
	return rec

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

		o 				response_jquery的参数
		url_ref 		redirect的参数
		**kwargs 		redirect的参数

	若请求通过普通表单提交，则调用redirect(url_ref, **kwargs)；
	若请求通过$submit提交，则调用response_jquery(o)。
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
