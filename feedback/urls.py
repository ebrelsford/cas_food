from django.conf.urls.defaults import patterns, url

from views import FeedbackResponseCreateView

urlpatterns = patterns('',
    url(r'^add/$', FeedbackResponseCreateView.as_view(),
        name='feedback_feedback_response_create'),
)
