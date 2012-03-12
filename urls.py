from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cas_food.views.home', name='home'),
    # url(r'^cas_food/', include('cas_food.foo.urls')),

    url(r'^$', 'schools.views.index'),
    url(r'^map/$', 'schools.views.map'),
    url(r'^schools/add/$', 'schools.views.add'),
    url(r'^schools/geojson', 'schools.views.as_geojson'),
    url(r'^schools/(?P<id>\d+)/$', 'schools.views.details'),

    url(r'^schools/(?P<id>\d+)/notes/add/$', 'content.views.add_note'),
    url(r'^schools/(?P<id>\d+)/pictures/add/$', 'content.views.add_picture'),
    url(r'^schools/(?P<id>\d+)/videos/add/$', 'content.views.add_video'),

    url(r'^menu/$', 'food.views.menu'),
    url(r'^menu/(?P<school_type>\w+)/$', 'food.views.menu'),
    #url(r'^menu/(?P<school_type>\w+)/(?P<year>\d+)/$', 'django.views.generic.date_based.archive_year'),
    url(r'^menu/(?P<school_type>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'food.views.menu_month'),
    url(r'^menu/(?P<school_type>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'food.views.menu_day'),
    url(r'^menu/dish/(?P<id>\d+)/$', 'food.views.details'),

    url(r'^admin/', include(admin.site.urls)),

    # auth
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/password/change/$', 'django.contrib.auth.views.password_change'),
    (r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^accounts/password/reset/$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/email=(?P<email>.*)$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password/reset/confirm?uid=(?P<uidb36>.*)&token=(?P<token>.*)$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),

)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns
