from django.conf.urls import patterns, url

from products import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^c(?P<pk>\d+)/$', views.new_comment_view, name='new_comment'),
    url(r'^order/$', views.new_order_view, name='new_order'),
)

