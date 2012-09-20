from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

import casfood_comments.urls as casfood_comments_urls
import connect.urls as connect_urls
import content.urls as content_urls
import feedback.urls as feedback_urls
import food.urls as food_urls
import getinvolved.urls as getinvolved_urls
import glossary.urls as glossary_urls
import pages.urls as pages_urls
import schools.urls as school_urls
import tray.urls as tray_urls
from views import IndexView

from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^schools/(?P<school_slug>[^/]+)/meals/', include(tray_urls)),
    url(r'^schools/(?P<school_slug>[^/]+)/follow/', 'accounts.views.follow'),
    url(r'^schools/(?P<school_slug>[^/]+)/unfollow/', 'accounts.views.unfollow'),
    url(r'^schools/', include(school_urls)),

    url(r'^menu/', include(food_urls)),
    url(r'^quiz/', include(feedback_urls)),

    url(r'^connect/', include(connect_urls)),
    url(r'^content/', include(content_urls)),
    url(r'^glossary/', include(glossary_urls)),
    url(r'^take-action/', include(getinvolved_urls)),
    url(r'^pages/', include(pages_urls)),

    url(r'^geo/geocode', 'geo.views.geocode'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^comments/', include(casfood_comments_urls)),

    # auth

    (r'^accounts/password/reset/$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/email=(?P<email>.*)$', 'accounts.views.password_reset'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^user/', include('accounts.urls')),

    (r'^selectable/', include('selectable.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns
    urlpatterns += staticfiles_urlpatterns()
