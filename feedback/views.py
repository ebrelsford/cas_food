from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView

from feedback import charts
from feedback.forms import FeedbackResponseForm
from generic.views import LoginRequiredMixin, PermissionRequiredMixin
from schools.models import School

class FeedbackResponseCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                                 CreateView):
    form_class = FeedbackResponseForm
    permission = 'feedback.add_feedbackresponse'
    template_name = 'feedback/create_feedback_response.html'

    def get_initial(self):
        initial = super(FeedbackResponseCreateView, self).get_initial()
        initial['added_by'] = self.request.user
        initial['school'] = School.objects.get(slug=self.kwargs['school_slug'])
        return initial

    def get_context_data(self, **kwargs):
        context = super(FeedbackResponseCreateView, self).get_context_data(**kwargs)
        context['school'] = School.objects.get(slug=self.kwargs['school_slug'])
        return context

    def get_success_url(self):
        slug = self.kwargs['school_slug']
        return reverse('schools.views.details', kwargs={ 'school_slug': slug })

class FeedbackResultsView(TemplateView):
    template_name = 'feedback/results.html'
    school = None

    def get_context_data(self, **kwargs):
        who, when = kwargs['who'], kwargs['when']

        try:
            school = School.objects.get(slug=kwargs['school_slug'])
        except Exception:
            school = None

        try:
            user = self.request.user
            if not user.is_authenticated():
                user = None
        except Exception:
            user = None

        chart_query_kwargs = {}

        if who == 'user' and user:
            chart_query_kwargs['added_by'] = user
        elif who == 'school' and school:
            chart_query_kwargs['school'] = school
        else:
            # don't restrict by user or school
            who = 'everywhere'

        if when == 'month':
            today = datetime.today()
            time_start = datetime(today.year, today.month, 1)

            chart_query_kwargs.update({
                'time_start': time_start,
                'time_end': time_start + relativedelta(months=1),
            })
        else:
            when = 'alltime'

        context = super(FeedbackResultsView, self).get_context_data(**kwargs)
        context.update({
            'school': school,

            'who': who,
            'when': when,

            'responses_count': charts._get_responses(**chart_query_kwargs).count(),

            'texture': {
                'data': json.dumps(charts.texture_data(**chart_query_kwargs).items()),
                'title': "What was the texture of the food today?",
            },
            'colors': {
                'data': json.dumps(charts.colors_data(**chart_query_kwargs).items()),
                'title': "How many colors were on your tray today?",
            },
            'finish': {
                'data': json.dumps(charts.finish_data(**chart_query_kwargs).items()),
                'title': "How much of your lunch did you finish today?",
                'subtitle': 'On a scale of 0 - 10',
            },
            'vegetables': {
                'data': json.dumps(charts.vegetables_data(**chart_query_kwargs).items()),
                'title': "How many vegetables were on your tray today?",
            },
            'energy': {
                'data': json.dumps(charts.energy_data(**chart_query_kwargs).items()),
                'title': "Were you sleepy or energetic after your meal?",
            },
        })
        return context
