from django.conf.urls import patterns, url

from products import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
    url(r'^(?P<pk_product>\d+)/$', views.detail_view, name='detail'),
    url(r'^c(?P<pk>\d+)/$', views.new_comment_view, name='new_comment'),
    url(r'^o(?P<pk>\d+)/$', views.new_order_view, name='new_order'),
)

