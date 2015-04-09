from django.conf.urls import patterns, url

from blogs import views

urlpatterns = patterns('',
	url(r'^$', views.list_view, name='list'),
	url(r'^(?P<pk_lawyer>\d+)/$', views.index_view, name='index'),
	url(r'^(?P<pk_lawyer>\d+)/archive\.(?P<year>\d+)-(?P<month>\d+)/$', views.index_archive_view, name='index_archive'),
	url(r'^(?P<pk_lawyer>\d+)/search/$', views.search_view, name='search'),
	url(r'^(?P<pk_lawyer>\d+)/search/(?P<query>[^/]+)$', views.search_view, name='search_alt'),
	url(r'^(?P<pk_lawyer>\d+)/tag\.(?P<tag>[^/]+)/$', views.index_tag_view, name='index_tag'),
	url(r'^category\.(?P<pk_category>\d+)/$', views.index_category_view, name='index_category'),
	url(r'^category\.(?P<pk_category>\d+)/remove/$', views.delete_category_view, name='delete_category'),
	url(r'^category\.(?P<pk_category>\d+)/rename/$', views.rename_category_view, name='rename_category'),
	url(r'^category\.new/$', views.categories_view, name='categories'),
	url(r'^home/$', views.home_view, name='home'),
	url(r'^text\.(?P<pk_text>\d+)/$', views.detail_view, name='text'),
	url(r'^text\.(?P<pk_text>\d+)/comment/$', views.new_comment_view, name='new_comment'),
	url(r'^text\.(?P<pk_text>\d+)/edit/$', views.edit_article_view, name='edit_article'),
	url(r'^text\.(?P<pk_text>\d+)/remove/$', views.delete_article_view, name='delete_article'),
	url(r'^text\.new/$', views.new_article_view, name='new_article'),

	url(r'^(?P<pk_lawyer>\d+)/archives\.mod$', views.archives_mod_view, name='archives_mod'),
	url(r'^(?P<pk_lawyer>\d+)/categories\.mod$', views.categories_mod_view, name='categories_mod'),
	url(r'^(?P<pk_lawyer>\d+)/favourites\.mod$', views.favourite_posts_mod_view, name='favourite_posts_mod'),
	url(r'^(?P<pk_lawyer>\d+)/recent_comments\.mod$', views.recent_comments_mod_view, name='recent_comments_mod'),
	url(r'^(?P<pk_lawyer>\d+)/tags\.mod$', views.tags_mod_view, name='tags_mod'),
)

