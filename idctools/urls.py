from django.conf.urls import include, url
from django.contrib import admin
from guangshuai_test.views  import *
urlpatterns = [
    # Examples:
    # url(r'^$', 'idctools.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
  #  url(r'^guangshuai_test/',include('guangshuai_test.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',index),
    url(r'^guangshuai_result/$',guangshuai_result),
    url(r'^test/$',test),
    url(r'^test2/$',test2),
    url(r'^module_number',module_number),
    url(r'^port_channel',port_channel),
    url(r'^ajax',data_ajax),
    url(r'^ping_monitor',ping_threading),
    url(r'^once_check',once_check),
]
