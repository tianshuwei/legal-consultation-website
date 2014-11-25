from django.conf.urls import patterns, url

from products import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
    # url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),,
)

