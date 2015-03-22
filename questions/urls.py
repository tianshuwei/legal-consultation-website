from django.conf.urls import patterns, url

from questions import views

urlpatterns = patterns('',
	url(r'^(?P<pk_question>\d+)/$', views.question_view, name='question'),
	url(r'^(?P<pk_question>\d+)/new_text/$', views.new_question_text_view, name='new_question_text'),
	url(r'^(?P<pk_question>\d+)/satisfied/$',views.question_satisfied,name='satisfied'),
	url(r'^new/$', views.new_question_view, name='new_question'),
)

