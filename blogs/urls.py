from django.conf.urls import patterns, url

from blogs import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'), # ListView
    url(r'^t(?P<pk>\d+)/$', views.text_view, name='text'), # DetailView
    url(r'^categories/$', views.categories_view, name='categories'), # ListView
    url(r'^new/$', views.new_article_view, name='new_article'),
)

