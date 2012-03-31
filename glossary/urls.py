from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView

from models import Entry

urlpatterns = patterns('',
    url(r'^$', ListView.as_view( 
            queryset=Entry.objects.all().order_by('title'),
        ),
        name='glossary_list'
    ),
    url(r'^add/$', 'glossary.views.create', name='glossary_entry_create'),
    url(r'^(?P<slug>.*)/edit/$', 'glossary.views.update', name='glossary_entry_update'),
    url(r'^(?P<slug>.*)/$', DetailView.as_view(
            model=Entry,
        ), 
        name='glossary_entry_detail'
    ),
)
