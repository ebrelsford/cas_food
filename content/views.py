from django.views.generic import ListView

from content.models import Picture

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
