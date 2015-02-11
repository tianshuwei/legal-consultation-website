from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
	url(r'^balance/$', views.balance_view, name='balance'),
	url(r'^lawyerlist/$', views.lawyerlist_view, name='lawyerlist'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^orders/(?P<pk_order>\d+)/$', views.order_detail_view, name='order_detail'),
	url(r'^orders/(?P<pk_order>\d+)/remove/$', views.order_delete_view, name='order_delete'),
	url(r'^profile\.(?P<pk_user>\d+)/$', views.profile_view, name='profile'),
	url(r'^profile/$', views.profile_self_view, name='profile_self'),
	url(r'^questions/(?P<pk_question>\d+)/$', views.question_view, name='question'),
	url(r'^questions/new/$', views.new_question_view, name='new_question'),
	url(r'^register/(?P<role>(client|lawyer))/$', views.register_view, name='register'),
	url(r'^remarks/(?P<pk_lawyer>\d+)/$', views.remark_view, name='remark'),
	url(r'^usercenter/$', views.usercenter_view, name='usercenter'),
	url(r'^questions/(?P<pk_question>\d+)/new_text/$', views.new_question_text_view, name='new_question_text'),
	url(r'^questions/(?P<pk_question>\d+)/satisfied/$',views.question_satisfied,name='satisfied'),
)

