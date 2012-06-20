from django.views.generic import ListView, UpdateView

from content.forms import SectionForm
from content.models import Picture, Section

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

class SectionUpdateView(UpdateView):
    model = Section
    form_class = SectionForm

    def get_form_kwargs(self):
        kwargs = super(SectionUpdateView, self).get_form_kwargs()
        # XXX will only work when editing an existing Section
        kwargs['object'] = self.get_object().content_object
        return kwargs

    def get_success_url(self):
        return self.get_object().content_object.get_absolute_url()
