from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView
from django.views.generic.create_update import update_object

from forms import DishForm
from models import Dish
from views import DayMenuView, MonthMenuView

urlpatterns = patterns('',
    url(r'^$', 'food.views.menu'),
    url(r'^(?P<school_type>\w+)/$', 'food.views.menu'),
    url(r'^(?P<school_type>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', MonthMenuView.as_view(), name='food_menu_month'),
    url(r'^(?P<school_type>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', DayMenuView.as_view(), name='food_menu_day'),

    url(r'^dish/(?P<slug>.*)/$', DetailView.as_view(
            model=Dish,
        ), 
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
