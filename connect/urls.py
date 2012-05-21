from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from models import Video, TwitterFeed
from views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='connect_index'),

    url(r'^video/$', ListView.as_view( 
            queryset=Video.objects.all().order_by('title'),
        ),
        name='connect_video_list'
    ),

    url(r'^twitter/$', ListView.as_view(
            queryset=TwitterFeed.objects.all().order_by('handle'),
        ),
        name='connect_twitterfeed_list'
    ),
)
