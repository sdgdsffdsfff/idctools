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
    url(r'^result/$',result)
]
