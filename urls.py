from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import glossary.urls as glossary_urls
import settings

urlpatterns = patterns('',
    url(r'^$', 'schools.views.index'),
    url(r'^map/$', 'schools.views.map'),
    url(r'^schools/geojson', 'schools.views.as_geojson'),
    url(r'^schools/(?P<id>\d+)/$', 'schools.views.details'),

    url(r'^schools/(?P<id>\d+)/notes/add/$', 'content.views.add_note'),
    url(r'^schools/(?P<id>\d+)/pictures/add/$', 'content.views.add_picture'),
    url(r'^schools/(?P<id>\d+)/videos/add/$', 'content.views.add_video'),

    url(r'^menu/$', 'food.views.menu'),
    url(r'^menu/(?P<school_type>\w+)/$', 'food.views.menu'),
    url(r'^menu/(?P<school_type>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'food.views.menu_month'),
    url(r'^menu/(?P<school_type>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'food.views.menu_day'),
    url(r'^menu/dish/(?P<slug>.*)/$', 'food.views.details'),

    url(r'^get-involved/$', 'getinvolved.views.index'),

    url(r'^glossary/', include(glossary_urls)),

    url(r'^geo/geocode', 'geo.views.geocode'),

    url(r'^admin/', include(admin.site.urls)),

    # auth

    (r'^accounts/password/reset/$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/email=(?P<email>.*)$', 'accounts.views.password_reset'),
    (r'^accounts/', include('registration.backends.default.urls')),

    (r'^selectable/', include('selectable.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns
