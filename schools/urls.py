from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^geojson', 'schools.views.as_geojson'),
    url(r'^(?P<school_slug>[^/]+)/$', 'schools.views.details'),
    url(r'^(?P<school_slug>[^/]+)/notes/add/$', 'schools.views.add_note'),
)
