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
	url(r'^order\.(?P<pk_order>\d+)/pay/$', views.order_complete_view, name='order_complete'),
	url(r'^order\.(?P<pk_order>\d+)/upload/$', views.upload_order_doc, name='order_upload'),
	url(r'^order\.(?P<pk_order>\d+)/query_contracts/$', views.query_order_contract_templates, name='order_query_contracts'),
	url(r'^order\.(?P<pk_order>\d+)/add_contract/$', views.add_order_contract_template, name='order_add_contract'),
	url(r'^order\.(?P<pk_order>\d+)/list_contracts/$', views.list_orderprocess_contract_templates, name='order_list_contracts'),
	url(r'^order\.(?P<pk_OPcontract>\d+)/del_OPcontract/$', views.remove_order_contract_template, name='order_del_contract'),
	url(r'^order\.(?P<pk_orderdoc>\d+)/del_uploaded/$', views.delete_order_doc, name='order_del_uploaded'),
	url(r'^order\.(?P<pk_order>\d+)/contract_form/$', views.order_contract_form, name='order_contract_form'),
	url(r'^orders/process/$', views.process_new_order_view, name='process_new_order'),
)
