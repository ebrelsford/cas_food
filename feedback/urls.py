from django.conf.urls.defaults import patterns, url

from views import FeedbackResponseCreateView, FeedbackResultsView

urlpatterns = patterns('',
    #url(r'^add/$',
    url(r'^schools/(?P<school_slug>[^/]+)/add/$',
        FeedbackResponseCreateView.as_view(),
        name='feedback_feedback_response_create',
    ),

    url(r'^results/$',
        FeedbackResultsView.as_view(),
        name='feedback_results',
    ),

    url(r'^results/month/$',
        FeedbackResultsView.as_view(
            timespan='month',
        ),
        name='feedback_results_month',
    ),

    url(r'^results/schools/(?P<school_slug>[^/]+)/$',
        FeedbackResultsView.as_view(),
        name='feedback_results_school',
    ),

    url(r'^results/schools/(?P<school_slug>[^/]+)/month/$',
        FeedbackResultsView.as_view(
            timespan='month',
        ),
        name='feedback_results_school_month',
    ),
)
