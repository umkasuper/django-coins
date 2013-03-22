# -*- coding: utf-8 -*-


import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from euro.views import euro, memorable
from euro.views import usa
from euro.views import russia
from euro.views import set_coins
from euro.sys   import site_logout


from registration.views import register, activate

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^euro/$', 'euro.views.euro', name='euro'),
    url(r'^usa/memorable/(?P<type>\S+)/$', usa, {'selectors': ["memorable"]}, name='usa_memorable'),
    url(r'^euro/memorable/(?P<country>\S+)$', memorable, {'selectors': ["euro", "memorable"]}, name='memorable'),
    url(r'^set/$', set_coins),
    url(r'^russia/$', russia),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include('registration.auth_urls')),
)
