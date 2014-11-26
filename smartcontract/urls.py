from django.conf.urls import patterns, url

from smartcontract import views

urlpatterns = patterns('',
    url(r'^test/$', views.test_render_view, name='test'),
)

