from django.conf.urls import patterns, url

from blogs import views

urlpatterns = patterns('',
	url(r'^$', views.home_view, name='home'),
	url(r'^all/$', views.list_view, name='list'),
	url(r'^(?P<pk_lawyer>\d+)/$', views.index_view, name='index'),
	url(r'^(?P<pk_lawyer>\d+)/(?P<pk_category>\d+)/$', views.index_category_view, name='index_category'),
	url(r'^c(?P<pk_text>\d+)/$', views.new_comment_view, name='new_comment'),
	url(r'^categories/$', views.categories_view, name='categories'),
	url(r'^categories/rm(?P<pk_category>\d+)/$', views.delete_category_view, name='delete_category'),
	url(r'^categories/mv(?P<pk_category>\d+)/$', views.rename_category_view, name='rename_category'),
	url(r'^t(?P<pk_text>\d+)/$', views.detail_view, name='text'),
	url(r'^text/rm(?P<pk_text>\d+)/$', views.delete_article_view, name='delete_article'),
	url(r'^text/ed(?P<pk_text>\d+)/$', views.edit_article_view, name='edit_article'),
	url(r'^text/new/$', views.new_article_view, name='new_article'),
)

