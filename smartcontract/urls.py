from django.conf.urls import patterns, url

from smartcontract import views

urlpatterns = patterns('',
    url(r'^test/$', views.test_render_view, name='test'),
    url(r'^render_form/(?P<pk_contract>\d+)/$', views.test_render_form_view),
    url(r'^test/pdf\.js/(?P<pk_contract>\d+)/$', views.test_pdf_view),
)

