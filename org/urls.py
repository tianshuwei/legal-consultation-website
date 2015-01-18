from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'index.views.index_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', include('index.urls',namespace='index')),
    url(r'^accounts/', include('accounts.urls',namespace='accounts')),
    url(r'^products/',include('products.urls',namespace='products')),
    url(r'^blogs/',include('blogs.urls',namespace='blogs')),
    url(r'^smartcontract/',include('smartcontract.urls',namespace='smartcontract')),
)

handler404 = 'index.views.my_custom_page_not_found_view'
