from django.conf.urls.defaults import patterns, url
from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_detail, object_list

from forms import EntryForm
from models import Entry

urlpatterns = patterns('',
    url(r'^$', 
        object_list, 
        {
            'queryset': Entry.objects.all().order_by('title'),
        }, 
        name='glossary_list'
    ),
    url(r'^add/$', 
        create_object, 
        {
            'login_required': True,
            'form_class': EntryForm,
        }, 
        name='glossary_entry_create'
    ),
    url(r'^(?P<slug>.*)/edit/$', 
        update_object, 
        {
            'login_required': True,
            'form_class': EntryForm,
        }, 
        name='glossary_entry_update'
    ),
    url(r'^(?P<slug>.*)/$', 
        object_detail,
        {
            'queryset': Entry.objects.all(),
        }, 
        name='glossary_entry_detail'
    ),
)
