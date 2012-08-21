from django.conf.urls.defaults import patterns, url

from views import FeedbackResponseCreateView, FeedbackResultsView

urlpatterns = patterns('',
    url(r'^schools/(?P<school_slug>[^/]+)/add/$',
        FeedbackResponseCreateView.as_view(),
        name='feedback_feedback_response_create',
    ),

    url(r'^results/(?:schools/(?P<school_slug>[^/]+)/)?(?:(?P<who>[^/]+)/)?(?:(?P<when>[^/]+)/)?$',
        FeedbackResultsView.as_view(),
        name='feedback_results',
    ),

)
