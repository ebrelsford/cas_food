from django.conf.urls.defaults import patterns, url

from pages.views import PageUpdateView

urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/edit/$', PageUpdateView.as_view(),
        name='pages_flatpage_update'
    ),
)
