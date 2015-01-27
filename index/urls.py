from django.conf.urls import patterns, url

from index import views

urlpatterns = patterns('',
	url(r'^$', views.index_view),
    url(r'^index/$', views.index_view, name='index'),
    url(r'^mod/(?P<name>.+)/$', views.mod_view),
    url(r'^transactions/$', views.transaction_record_view),
)

