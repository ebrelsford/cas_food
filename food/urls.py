from django.conf.urls.defaults import patterns, url
from django.views.generic.create_update import update_object
from django.views.generic.list_detail import object_detail

from forms import DishForm
from models import Dish

urlpatterns = patterns('',
    url(r'^dish/(?P<slug>.*)/$', 
        object_detail,
        {
            'queryset': Dish.objects.all(),
        }, 
        name='food_dish_detail'
    ),
    # TODO complete--not working currently
    url(r'^dish/(?P<slug>.*)/edit/$', 
        update_object,
        {
            'form_class': DishForm,
            #'slug_field': 'slug',
        }, 
        name='food_dish_update'
    ),
)
