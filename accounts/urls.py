from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
	url(r'^lawyerlist/$', views.lawyerlist_view, name='lawyerlist'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^login4siege/$', views.siege_view),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^profile\.(?P<pk_user>\d+)/$', views.profile_view, name='profile'),
	url(r'^questions/(?P<pk_question>\d+)/$', views.question_view, name='question'),
	url(r'^questions/(?P<pk_question>\d+)/new_text/$', views.new_question_text_view, name='new_question_text'),
	url(r'^questions/(?P<pk_question>\d+)/satisfied/$',views.question_satisfied,name='satisfied'),
	url(r'^questions/new/$', views.new_question_view, name='new_question'),
	url(r'^register/(?P<role>(client|lawyer))/$', views.register_view, name='register'),
	url(r'^remarks/(?P<pk_lawyer>\d+)/$', views.remark_view, name='remark'),
	url(r'^usercenter/$', views.usercenter_view, name='usercenter'),
	url(r'^usercenter/balance/$', views.balance_view, name='balance'),
	url(r'^usercenter/orders/$',  views.orders_view, name='order_list'),
	url(r'^usercenter/profile/$', views.profile_self_view, name='profile_self'),
	url(r'^usercenter/questions/$', views.questions_view , name='question_list'),
)

