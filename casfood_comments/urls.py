from django.conf.urls.defaults import patterns, url

from casfood_comments.views import CommentDeleteView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/delete/$',
        CommentDeleteView.as_view(),
        name='comments_comment_delete'
    ), 
)
