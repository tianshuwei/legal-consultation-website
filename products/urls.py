from django.conf.urls import patterns, url

from products import views

urlpatterns = patterns('',
	url(r'^$', views.index_view, name='index'),
	url(r'^(?P<pk_product>\d+)/$', views.detail_view, name='detail'),
	url(r'^(?P<pk_product>\d+)/comment/$', views.new_comment_view, name='new_comment'),
	url(r'^(?P<pk_product>\d+)/order/$', views.new_order_view, name='new_order'),
	url(r'^order\.(?P<pk_order>\d+)/$', views.order_detail_view, name='order_detail'),
	url(r'^order\.(?P<pk_order>\d+)/remove/$', views.order_delete_view, name='order_delete'),
	url(r'^order\.(?P<pk_order>\d+)/pay/$', views.order_pay_view, name='order_pay'),
)

