from django.conf.urls import patterns, url

from blogs import views

urlpatterns = patterns('',
	url(r'^$', views.home_view, name='home'),
	url(r'^(?P<pk_lawyer>\d+)/$', views.index_view, name='index'),
	url(r'^(?P<pk_lawyer>\d+)/(?P<pk_category>\d+)/$', views.index_category_view, name='index_category'),
	url(r'^t(?P<pk_text>\d+)/$', views.detail_view, name='text'),
	url(r'^c(?P<pk_text>\d+)/$', views.new_comment_view, name='new_comment'),
	url(r'^categories/$', views.categories_view, name='categories'),
	url(r'^new/$', views.new_article_view, name='new_article'),
	url(r'^e(?P<pk_text>\d+)/$', views.edit_article_view, name='edit_article'),
	url(r'^del(?P<pk_text>\d+)/$', views.delete_article_view, name='delete_article'),
)

