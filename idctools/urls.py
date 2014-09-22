from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'idctools.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
  #  url(r'^guangshuai_test/',include('guangshuai_test.urls')),
    url(r'^guangshuai_test/', include('guangshuai_test.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/',include('guangshuai_test.urls')),
]
