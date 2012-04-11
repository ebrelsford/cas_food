from django.conf.urls.defaults import patterns, url
from django.contrib.flatpages.models import FlatPage
from django.views.generic import UpdateView

from forms import FlatPageForm

urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/edit/$', UpdateView.as_view(
            model=FlatPage,
            form_class=FlatPageForm,
        ),
        name='flatpages_flatpage_update'
    ),
)
