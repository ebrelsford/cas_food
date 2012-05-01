from django.core.urlresolvers import reverse
from django.views.generic import CreateView

from generic.views import LoginRequiredMixin, PermissionRequiredMixin
from schools.models import School
from forms import FeedbackResponseForm

class FeedbackResponseCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                                 CreateView):
    form_class = FeedbackResponseForm
    permission = 'feedback.create_feedback_response'
    template_name = 'feedback/create_feedback_response.html'

    def get_initial(self):
        print 'get_initial'
        initial = super(FeedbackResponseCreateView, self).get_initial()
        initial['added_by'] = self.request.user
        initial['school'] = School.objects.get(slug=self.kwargs['school_slug'])
        return initial

    def get_success_url(self):
        slug = self.kwargs['school_slug']
        return reverse('schools.views.details', kwargs={ 'school_slug': slug })
