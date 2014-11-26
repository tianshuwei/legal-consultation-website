from django.conf.urls import patterns, url

from products import views

urlpatterns = patterns('',
    # url(r'^$', views.index_view, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),,
)

