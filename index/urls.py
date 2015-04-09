from django.conf.urls import patterns, url

from index import views

urlpatterns = patterns('',
	url(r'^$', views.index_view),
    url(r'^index/$', views.index_view, name='index'),
    url(r'^mod/(?P<name>.+)/$', views.mod_view),
    url(r'^transactions/$', views.transaction_record_view),
    url(r'^lpub.hex$', views.login_pubkey_view),

    url(r'base/popular_blog_articles\.mod', views.popular_blog_articles_mod_view, name='popular_blog_articles_mod'),
    url(r'base/new_members\.mod', views.new_members_mod_view, name='new_members_mod'),
)

