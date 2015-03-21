from django.conf.urls import patterns, include, url
from django.contrib import admin
from org.settings import DEBUG, MEDIA_ROOT

urlpatterns = patterns('',
	# url(r'^$', 'index.views.index_view'),
	url(r'^', include('index.urls',namespace='index')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('accounts.urls',namespace='accounts')),
	url(r'^products/', include('products.urls',namespace='products')),
	url(r'^blogs/', include('blogs.urls',namespace='blogs')),
	url(r'^smartcontract/', include('smartcontract.urls',namespace='smartcontract')),
)

if DEBUG:
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
	)

handler404 = 'index.views.my_custom_page_not_found_view'
