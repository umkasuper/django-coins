# -*- coding: utf-8 -*-


import settings
from django.conf.urls import patterns, include, url

from euro.views import euro, euro_memorable
from euro.views import usa
from euro.views import russia
from euro.views import set_coins
from euro.sys   import site_logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coins.views.home', name='home'),
    # url(r'^coins/', include('coins.foo.urls')),

    url(r'^euro/$', euro),
    url(r'^euro_memorable/$', euro_memorable),
    url(r'^set/$', set_coins),
    url(r'^usa/$', usa),
    url(r'^russia/$', russia),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', site_logout),
#    url(r'^accounts/profile/$', 'django.contrib.auth.views.profile'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
