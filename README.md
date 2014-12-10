# README

## 公告

settings.py加入git同步，不一样的部分被放到了org/deployment.py。示例如下：

~~~python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'enq9o3g*0w(d)bpivhhuns+z96i=bcn)a$dz_^plfpgp$1-99^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'org_dev',
		'HOST': 'localhost',
		'USER': 'org_dev',
		'PASSWORD': 'org_dev',
		'PORT': '3306',
		'CHARSET': 'utf8'
	}
}
~~~


## 本周计划

3. 产品模块设计
3. 咨询提问、评价
5. 用户中心初步
6. 导航栏设计
5. 统计功能需求分析（把触发器设计进去）

## 下一步计划

1. 用户中心、律师中心
4. blogs, products测试
7. blogs 搜索、标签

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

** 第四周 **

1. UI模板设计
2. tanki UI模板设计
4. alex 律师博客 _页面设计_
2. view重构
3. 关系模式调整

## 全站关系模式

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
