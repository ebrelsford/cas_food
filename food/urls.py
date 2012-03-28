from django.conf.urls.defaults import patterns, url
from django.views.generic.list_detail import object_detail

from models import Dish

urlpatterns = patterns('',
    url(r'dish/(?P<slug>.*)/$', 
        object_detail,
        {
            'queryset': Dish.objects.all(),
        }, 
        name='food_dish_detail'
    ),
)
