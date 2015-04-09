# -*- coding: utf-8 -*-
from org.tools import *
from accounts.models import Lawyer
from products.models import Product
from accounts.models import Client
from index.models import TransactionRecord
from blogs.models import BlogArticle

def index_view(request):
	return response(request,'index/index.html',
		latest_products_list=Product.objects.order_by('-publish_date')[:5]
	)

def my_custom_page_not_found_view(request):
	return response(request,'index/404.html')

def transaction_record_view(request):
	return response(request, 'index/transaction_record.html',
		records=TransactionRecord.objects.all()
	)

def login_pubkey_view(request):
	from org.settings import RSA_LOGIN_KEY
	pubkey, privkey = RSA_LOGIN_KEY
	return HttpResponse(hex(pubkey.n)[2:-1], content_type="text/plain")

def mod_view(request, name):
	"""templates/mod下的*.html文件允许访问，URL是 /mod/*/"""
	try: return response(request, 'mod/{0}.html'.format(name))
	except: handle_illegal_access(request)

def popular_blog_articles_mod_view(request):
	return response(request, 'popular_blog_articles.mod.html',
		popular_blog_articles=BlogArticle.objects.get_popular_articles())

def new_members_mod_view(request):
	return response(request, 'new_members.mod.html',
		new_members=Client.objects.get_latest_reg_user())
