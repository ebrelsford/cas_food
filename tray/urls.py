from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^add/$', 'tray.views.add'),
    url(r'^(?P<tray_id>\d+)/$', 'tray.views.details'),
    url(r'^(?P<tray_id>\d+)/comments/add/$', 'tray.views.add_comment'),
    url(r'^(?P<tray_id>\d+)/rate/', 'tray.views.rate'),
)
