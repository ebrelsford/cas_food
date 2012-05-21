from random import sample

from django.views.generic import TemplateView

from models import TwitterFeed, Video

class IndexView(TemplateView):
    template_name = 'connect/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['videos'] = self._pick_videos(3)
        context['twitterfeeds'] = self._pick_twitterfeeds(3)
        return context

    def _pick_twitterfeeds(self, count):
        feeds = TwitterFeed.objects.all().order_by('handle')
        feed_count = feeds.count()
        indices = sorted(sample(xrange(feed_count), min(feed_count, count)))
        return [feeds[i] for i in indices]

    def _pick_videos(self, count):
        videos = Video.objects.all().order_by('title')
        video_count = videos.count()
        indices = sorted(sample(xrange(video_count), min(video_count, count)))
        return [videos[i] for i in indices]
