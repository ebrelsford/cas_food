from django.http import Http404
from django.views.generic import ListView, UpdateView

from content.forms import SectionForm
from content.models import Picture, Section
from generic.views import LoginRequiredMixin, PermissionRequiredMixin

class PictureListView(ListView):
    default_count = 3
    default_index = 0

    def get_queryset(self):
        count = int(self.request.GET.get('count', self.default_count))
        index = int(self.request.GET.get('index', self.default_index))
        if index < 0:
            return Picture.objects.none()

        pictures = Picture.objects.all().order_by('-added')

        if count > pictures.count():
            return pictures
        return pictures[index:index + count]

class SectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = SectionForm
    model = Section
    permission = 'content.change_section'

    def get_form_kwargs(self):
        kwargs = super(SectionUpdateView, self).get_form_kwargs()
        try:
            kwargs['object'] = self.get_object().content_object
        except Exception:
            raise Http404
        return kwargs

    def get_success_url(self):
        return self.get_object().content_object.get_absolute_url()
