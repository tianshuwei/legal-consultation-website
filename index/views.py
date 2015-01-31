# -*- coding: utf-8 -*-
from org.tools import *
from accounts.models import Lawyer
from products.models import Product
from index.models import TransactionRecord

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

def mod_view(request, name):
	"""templates/mod下的*.html文件允许访问，URL是 /mod/*/"""
	try: return response(request, 'mod/{0}.html'.format(name))
	except: raise Http404
