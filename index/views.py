# -*- coding: utf-8 -*-
from org.tools import *
from accounts.models import Lawyer
from products.models import Product

def index_view(request):
	return response(request,'index/index.html',
		latest_products_list=Product.objects.order_by('-publish_date')[:5]
	)

