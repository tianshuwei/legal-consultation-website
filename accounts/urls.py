from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^register_(?P<role>(client|lawyer))/$', views.register_view, name='register'),
	url(r'^lawyerlist/$', views.lawyerlist_view, name='lawyerlist'),
	url(r'^usercenter/$', views.usercenter_view, name='usercenter'),
	url(r'^profile/$', views.profile_view, name='profile'),
	url(r'^q(?P<pk>\d+)/$', views.question_view, name='question'),
	url(r'^o(?P<pk>\d+)/$', views.order_detail_view, name='order_detail'),
	url(r'^balance/$', views.balance_view, name='balance'),
	url(r'^r(?P<pk>\d+)/$', views.remark_view, name='remark'), # pk->user.id (lawyer)
	url(r'^question/$', views.new_question_view, name='new_question'),
)

