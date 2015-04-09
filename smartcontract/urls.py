from django.conf.urls import patterns, url

from smartcontract import views

urlpatterns = patterns('',
    url(r'^test/$', views.test_render_view, name='test'),
    url(r'^detail/(?P<pk_contract>\d+)/$', views.test_render_form_view,name='detail'),
    url(r'^test/pdf\.js/(?P<pk_contract>\d+)/$', views.test_pdf_view),
    url(r'^index/$', views.index_view,name='index'),

    url(r'^download409/(?P<pk_contract>\d+)/$', views.download_0409_view, name='download409'),
)

