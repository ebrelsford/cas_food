from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView

from models import Dish
from views import DayMenuView, DishUpdateView, MonthMenuView, DishAddPictureView

urlpatterns = patterns('',
    url(r'^$', 'food.views.menu'),

    url(r'^(?P<school_type>[\w,]+)/$', 'food.views.menu'),

    url(r'^(?P<school_type>[\w,]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        MonthMenuView.as_view(), name='food_menu_month'),

    url(r'^(?P<school_type>[\w,]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        DayMenuView.as_view(), name='food_menu_day'),

    url(r'^dish/(?P<slug>[^/]*)/$', 
        DetailView.as_view(
            model=Dish,
        ), 
        name='food_dish_detail'
    ),

    url(r'^dish/(?P<slug>[^/]*)/picture/add/$', DishAddPictureView.as_view(),
        name='food_dish_add_picture'),

    url(r'^dish/(?P<slug>[^/]*)/edit/$', DishUpdateView.as_view(),
        name='food_dish_update'),

    url(r'^ingredients/add/(?P<name>[^/]*)/$',
        'food.views.add_or_get_ingredient'),

    url(r'^nutrients/add/(?P<name>[^/]*)/$', 'food.views.add_or_get_nutrient'),
)
