# README
 
## 公告

> 鉴于Django对View的封装存在诸多不足，决定取消generic view的使用，
> org/tools.py中有自己封装的写view的API，用法参考blogs应用。
> 

_org/tools.py_

~~~python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render

def redirect(url_ref,**kwargs):
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
	return HttpResponse(loader.get_template(template_name).render(RequestContext(request, context)))

def checkf(exp, default=None):
	"""
	求lambda表达式的值，异常返回default（默认为None）

		exp            一个无参lambda表达式
		default        异常返回默认值
	""" 
	try: return exp()
	except: return default

"""
views.py中使用

from org.tools import *

之后这些下面的包自动导入
"""

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import get_object_or_404
~~~

_Example_

~~~python
from org.tools import * # important! 导入写view用的API
# ... 然后导入用到的关系模式

# ...

def home_view(request):
	try: return redirect('blogs:index', pk_lawyer=request.user.lawyer.id) # HTTP重定向
	except ObjectDoesNotExist, e: raise Http404 # 引发HTTP错误

def index_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	return response(request, 'blogs/index.html',  # 常规HTTP响应
		lawyer=lawyer,
		is_master=checkf(lambda: request.user.lawyer==lawyer),
		categories=BlogCategory.objects.filter(user=pk_lawyer),
		latest_blogs_list=BlogArticle.objects.filter(author=pk_lawyer).order_by('-publish_date'))

# ...

~~~

## 本周计划

1. UI模板设计
2. tanki UI模板设计
3. timothy 产品 订单 _页面设计_
4. alex 律师博客 _页面设计_
2. view重构
3. 关系模式调整

## 下一步计划

1. 用户中心、律师中心 _页面设计_
3. timothy 咨询提问、评价 _页面设计_
4. blogs, products测试
5. 用户中心初步
5. 统计功能需求分析（把触发器设计进去）
6. 导航栏设计
7. blogs 分页显示、搜索、标签

## 计划历史

** 第一周 **

1. 创建关系模式以及数据库表
2. 用户注册/登入、主页

** 第二周 **

1. 实现关系模式中的多对多关系
2. 规划网站的页面设计
3. 完善关系模式

** 第三周 **

1. Django数据库表相关实验
2. products模块列表/详细页，用户评论
3. 用户对律师的的咨询提问、评价 (未完)

## 全站URL设计  2014.12.2

~~~python
# org/urls.py
	url(r'^admin/', include(admin.site.urls)),
	url(r'^index/', include('index.urls',namespace='index')),
	url(r'^accounts/', include('accounts.urls',namespace='accounts')),
	url(r'^products/',include('products.urls',namespace='products')),
	url(r'^blogs/',include('blogs.urls',namespace='blogs')),
	url(r'^smartcontract/',include('smartcontract.urls',namespace='smartcontract')),

# accounts/urls.py
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^register/$', views.register_view, name='register'),
	url(r'^lawyerlist/$', views.lawyerlist_view, name='lawyerlist'), # ListView
	url(r'^usercenter/$', views.usercenter_view, name='usercenter'),
	url(r'^lawyercenter/$', views.lawyercenter_view, name='lawyercenter'),
	url(r'^profile/$', views.profile_view, name='profile'), # DetailView
	url(r'^q(?P<pk>\d+)/$', views.question_view, name='question'), # DetailView
	url(r'^o(?P<pk>\d+)/$', views.order_detail_view, name='order_detail'), #DetailView
	url(r'^balance/$', views.balance_view, name='balance'),
	url(r'^r(?P<pk>\d+)/$', views.remark_view, name='remark'), # pk->user.id (lawyer)
	url(r'^question/$', views.new_question_view, name='new_question'),

# blogs/urls.py
	url(r'^$', views.home_view, name='home'),
	url(r'^(?P<pk_lawyer>\d+)/$', views.index_view, name='index'),
	url(r'^(?P<pk_lawyer>\d+)/(?P<pk_category>\d+)/$', views.index_category_view, name='index_category'),
	url(r'^c(?P<pk_text>\d+)/$', views.new_comment_view, name='new_comment'),
	url(r'^categories/$', views.categories_view, name='categories'),
	url(r'^categories/rm(?P<pk_category>\d+)/$', views.delete_category_view, name='delete_category'),
	url(r'^categories/mv(?P<pk_category>\d+)/$', views.rename_category_view, name='rename_category'),
	url(r'^t(?P<pk_text>\d+)/$', views.detail_view, name='text'),
	url(r'^text/rm(?P<pk_text>\d+)/$', views.delete_article_view, name='delete_article'),
	url(r'^text/ed(?P<pk_text>\d+)/$', views.edit_article_view, name='edit_article'),
	url(r'^text/new/$', views.new_article_view, name='new_article'),

# index/urls.py
	url(r'^$', views.index_view, name='index'),

# products/urls.py
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^c(?P<pk>\d+)/$', views.new_comment_view, name='new_comment')
	url(r'^order/$', views.new_order_view, name='new_order'),

# smartcontract/urls.p
	url(r'^test/$', views.test_render_view, name='test'),

~~~

## 全站关系模式（非主属性可能不全）

> User(ID,username,password) （Django内置用户模块）
> 
> Client(ID,user,balance,points)
> 
> Lawyer(ID,user,balance,blacklist,score,blog) 
> 
> Product(ID,name,publish_date,description,price)
> 
> Remark(ID,c_id,l_id,grade,date)
> 
> Question(ID,c_id,l_id,title,text,date)
> 
> Question_text(ID,user_id,user_flag,text,date)
> 
> Comment(ID,c_id,p_id,comment,date)
> 
> Order(ID,c_id,l_id,p_id,state,start_date)
> 
> BlogCategory(ID,user,name)
> 
> BlogArticle(ID,title,publish_date,category,tags,text)
> 
> BlogComment(ID,user,publish_date,article,text)
> 

## 全站页面设计

![网站页面设计](https://bytebucket.org/spuerme/org/raw/082d7d30a94a1f56864a69fa6a1d287c0d49f050/docs/pages.png?token=20eb985de976b86c08f6bf93e3ce74571b682005)

## 服务器资源

** 222.69.93.107 服务器(调试)端口分配 **

> 6001 - alex
> 
> 6002 - timothy
> 
> 6003 - tanki
> 

** 222.69.93.107 服务器数据库初始化参考 **

> create database org\_dev character set utf8;
> 
> create database org\_alex character set utf8;
> 
> create database org\_timothy character set utf8;
> 
> create database org\_tanki character set utf8;
> 
> grant all privileges on org\_alex.* to org\_alex@'localhost' identified by 'org\_alex';
> 
> grant all privileges on org\_tanki.* to org\_tanki@'localhost' identified by 'org\_tanki';
> 
> grant all privileges on org\_tanki.* to org\_tanki@'%' identified by 'org\_tanki';
> 
> grant all privileges on org\_timothy.* to org\_timothy@'%' identified by 'org\_timothy';
> 
> grant all privileges on org\_timothy.* to org\_timothy@'localhost' identified by 'org\_timothy';
> 
> grant all privileges on org\_dev.* to org\_dev@'localhost' identified by 'org\_dev';
> 
> grant all privileges on org\_dev.* to org\_dev@'%' identified by 'org\_dev';
> 
> flush privileges;
> 

'org\_dev'作为公用数据库、数据库账户、数据库密码
，为了方便隔离调试环境，也可以使用其他几个账户对应的数据库。


## 说明

默认情况下，
项目所有源代码、数据库采用了UTF-8编码；
python源代码使用制表符缩进，UNIX风格换行符换行；
模板、URL、静态文件均按照Django约定的命名空间配置。

settings.py已通过.gitignore设置为忽略，因为settings.py与调试/部署环境密切相关，没有同步的意义。如果需要参考数据库配置，参考同目录下settings-sample.py。

开发过程遇到问题留意最后的参考链接，参考链接会随项目开发进程不断更新。

## 参考 

** Django官方文档速查 **

- Part1 [创建关系模式/更新数据库/ORM API](https://docs.djangoproject.com/en/1.7/intro/tutorial01/)
- Part2 [创建应用/自定义后台](https://docs.djangoproject.com/en/1.7/intro/tutorial02/)
- Part3 [URL模型/响应请求/模板系统](https://docs.djangoproject.com/en/1.7/intro/tutorial03/)
- Part4 [处理表单](https://docs.djangoproject.com/en/1.7/intro/tutorial04/)
- Part5 [单元测试](https://docs.djangoproject.com/en/1.7/intro/tutorial05/)
- Part6 [静态文件](https://docs.djangoproject.com/en/1.7/intro/tutorial06/)
- [创建关系模式](https://docs.djangoproject.com/en/1.7/ref/models/relations/)
- [Django的多对多关系/数据库数据类型](https://docs.djangoproject.com/en/1.7/ref/models/fields/#manytomanyfield)
- [数据库查询](https://docs.djangoproject.com/en/1.7/topics/db/queries/)
- [渲染表单](https://docs.djangoproject.com/en/1.7/topics/forms/)
- [Django认证系统](https://docs.djangoproject.com/en/1.7/topics/auth/default/)

** 站点管理 **

- [Django管理常用命令](http://www.oschina.net/question/234345_54799)

** Django ORM参考 **

- [Django的多对多关系](https://docs.djangoproject.com/en/1.7/ref/models/fields/#manytomanyfield)
- [理解django的多对多ManyToManyField](http://luozhaoyu.iteye.com/blog/1510635)

** Git 如何使用 **

- [Git分支的常见的管理](http://libin52008.blog.163.com/blog/static/1053271872013313105039787/)
- [Git分支管理和冲突解决](http://www.cnblogs.com/mengdd/p/3585038.html)

** Django 用户权限模块 **

- [总结Django中的用户权限模块](http://maplye.iteye.com/blog/448960)
- [Django认证系统](https://docs.djangoproject.com/en/1.7/topics/auth/default/)

** 站点部署 **

- [How to use Django with uWSGI](https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/uwsgi/)
- [Setting up Django and your web server with uWSGI and nginx](http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)
- [Django uwsgi Nginx组合建站](http://blog.chinaunix.net/uid-11390629-id-3610722.html)
