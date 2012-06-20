from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView

from content.models import Section
from content.views import PictureListView, SectionUpdateView

urlpatterns = patterns('',
    url(r'^pictures/', PictureListView.as_view(),
        name='content_pictures_list'
    ),

    url(r'^sections/(?P<pk>\d+)/$', DetailView.as_view(
            model=Section,
        ), 
        name='content_section_detail'
    ),

    url(r'sections/(?P<pk>\d+)/edit/$', SectionUpdateView.as_view(),
        name='content_section_update'
    ),
)
