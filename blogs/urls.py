from django.conf.urls import patterns, url

from blogs import views

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', views.IndexView.as_view(), name='index'), # ListView pk->user.id (lawyer)
    url(r'^t(?P<pk>\d+)/$', views.DetailView.as_view(), name='text'), # DetailView
    url(r'^c(?P<pk>\d+)/$', views.new_comment_view, name='new_comment'),
    url(r'^categories/$', views.categories_view, name='categories'), # ListView
    url(r'^new/$', views.new_article_view, name='new_article'),
)

