from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'org.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', include('index.urls',namespace='index')),
    url(r'^accounts/', include('accounts.urls',namespace='accounts')),
    url(r'^products/',include('products.urls',namespace='products')),
)
