# -*- coding: utf-8 -*-


import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from euro.views import euro, memorable
from euro.views import all_memorable
from euro.views import set_coins

from euro.sys import site_logout
from euro.api_v1 import api_v1_euro_list_countries, api_v1_euro_list_years, api_v1_euro_what

#from registration.views import register, activate

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^pdf/euro/memorable/(?P<year>\d{4})$', memorable, {'selectors': ["euro", "memorable"], 'country': "all", "pdf" :True}, name='pdf_year'),
    url(r'^pdf/euro/memorable/(?P<country>\S+)$', memorable, {'selectors': ["euro", "memorable"], "pdf": True}, name='pdf_memorable'),

    url(r'^$', memorable, {'selectors': ["euro", "memorable"], 'country': "all", 'year': '2015'}, name='year'),

    url(r'^euro/$', 'euro.views.euro', name='euro'),
    url(r'^euro/memorable/(?P<year>\d{4})$', memorable, {'selectors': ["euro", "memorable"], 'country': "all"}, name='year'),
    url(r'^euro/memorable/(?P<country>\S+)$', memorable, {'selectors': ["euro", "memorable"]}, name='memorable'),
    #url(u'^(?P<country>\S+)/memorable/(?P<type>\S+)/$', usa, {'selectors': ['memorable']}, name='country_memorable'),
    url(u'^(?P<country>\S+)/memorable/(?P<type>[-\w\ ]+)/$', all_memorable, {'selectors': ['memorable']}, name='country_memorable'),
    url(r'^set/$', set_coins),

    url(r'^api/v1/euro/list_countries', api_v1_euro_list_countries),
    url(r'^api/v1/euro/list_years', api_v1_euro_list_years),
    url(r'^api/v1/euro/what', api_v1_euro_what),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include('registration.auth_urls')),
)
