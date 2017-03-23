# -*- coding: utf-8 -*-

import coins.settings

from django.conf.urls import include, url

from django.views.generic import TemplateView

from euro.views import euro, memorable, all_memorable, set_coins

from euro.sys import site_logout

from euro.api_v1 import api_v1_euro_list_countries, api_v1_euro_list_years, api_v1_euro_what, api_v1_euro_save

#from registration.views import register, activate

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.views.static import serve


from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^pdf/euro/memorable/(?P<year>\d{4})$', memorable, {'selectors': ["euro", "memorable"], 'country': "all", "pdf" :True}, name='pdf_year'),
    url(r'^pdf/euro/memorable/(?P<country>\S+)$', memorable, {'selectors': ["euro", "memorable"], "pdf": True}, name='pdf_memorable'),
    url(u'^pdf/(?P<country>\S+)/memorable/(?P<type>[-\w\ ]+)/$', all_memorable, {'selectors': ['memorable']}, name='pdf_grouped_memorable'),

    url(r'^$', memorable, {'selectors': ["euro", "memorable"], 'country': "all", 'year': '2017'}, name='year'),

    url(r'^euro/regular/(?P<country>\S+)/(?P<year>\d{4})$', euro, name='regular_year'),
    url(r'^euro/regular/(?P<country>\S+)$', euro, name='euro'),
    url(r'^euro/memorable/(?P<year>\d{4})$', memorable, {'selectors': ["euro", "memorable"], 'country': "all"}, name='year'),
    url(r'^euro/memorable/(?P<country>\S+)$', memorable, {'selectors': ["euro", "memorable"]}, name='memorable'),
    #url(u'^(?P<country>\S+)/memorable/(?P<type>\S+)/$', usa, {'selectors': ['memorable']}, name='country_memorable'),
    url(u'^(?P<country>\S+)/memorable/(?P<type>[-\w\ ]+)/$', all_memorable, {'selectors': ['memorable']}, name='country_memorable'),
    url(r'^set/$', set_coins),

    url(r'^api/v1/euro/list_countries', api_v1_euro_list_countries),
    url(r'^api/v1/euro/list_years', api_v1_euro_list_years),
    url(r'^api/v1/euro/what', api_v1_euro_what),
    url(r'^api/v1/euro/save', api_v1_euro_save),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': coins.settings.MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': coins.settings.MEDIA_ROOT}),

##    url(r'^accounts/', include('registration.backends.default.urls')),
#    url(r'^accounts/login/$', auth_views.login),
#    url(r'', include('registration.auth_urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url('^', include('django.contrib.auth.urls')),
]
