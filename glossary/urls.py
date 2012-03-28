from django.conf.urls.defaults import patterns, url
from django.views.generic.list_detail import object_detail, object_list

from models import Entry

urlpatterns = patterns('',
    url(r'^$', 
        object_list, 
        {
            'queryset': Entry.objects.all().order_by('title'),
        }, 
        name='glossary_list'
    ),
    url(r'^add/$', 'glossary.views.create', name='glossary_entry_create'),
    url(r'^(?P<slug>.*)/edit/$', 'glossary.views.update', name='glossary_entry_update'),
    url(r'^(?P<slug>.*)/$', 
        object_detail,
        {
            'queryset': Entry.objects.all(),
        }, 
        name='glossary_entry_detail'
    ),
)
