from random import randint

from django.views.generic import TemplateView

from connect.models import Video
from content.models import Picture

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['video'] = self._pick_video()
        context['pictures_count'] = self._get_pictures_count()
        return context

    def _get_pictures_count(self):
        return Picture.objects.all().count()

    def _pick_video(self):
        video_count = Video.objects.all().count()
        random_index = randint(0, video_count - 1)
        return Video.objects.all()[random_index]
