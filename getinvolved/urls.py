from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView

from models import Post
from views import PostCreateView, PostUpdateView

urlpatterns = patterns('',
    url(r'^$', ListView.as_view( 
            queryset=Post.objects.all(),
        ),
        name='getinvolved_post_list'
    ),
    url(r'^posts/add/$', PostCreateView.as_view(), name='getinvolved_post_create'),
    url(r'^posts/(?P<pk>\d+)/edit/$', PostUpdateView.as_view(), name='getinvolved_post_update'),
    url(r'^posts/(?P<pk>\d+)/$', DetailView.as_view(
            model=Post,
        ), name='getinvolved_post_detail'
    ),
)
