from django.conf.urls.defaults import patterns, url

from content.views import PictureListView

urlpatterns = patterns('',
    url(r'^pictures/', PictureListView.as_view(),
        name='content_pictures_list'
    ),
)
