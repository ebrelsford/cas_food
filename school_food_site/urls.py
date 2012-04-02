from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

import food.urls as food_urls
import glossary.urls as glossary_urls
import schools.urls as school_urls
import tray.urls as tray_urls

import settings

urlpatterns = patterns('',
    url(r'^$', 'schools.views.index'),
    url(r'^map/$', 'schools.views.map'),
    url(r'^schools/(?P<school_slug>[^/]+)/meals/', include(tray_urls)),
    url(r'^schools/', include(school_urls)),

    url(r'^menu/', include(food_urls)),

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
    urlpatterns += staticfiles_urlpatterns()
