from django.conf.urls.defaults import patterns, url

from views import DayMenuView, DishDetailView, DishUpdateView, MonthMenuView,\
        DishAddPictureView, MealListView

urlpatterns = patterns('',
    url(r'^$', 'food.views.menu'),

    url(r'^today/$', 'food.views.todays_menu'),

    url(r'^(?P<school_type>[\w,]+)/$', 'food.views.menu'),

    url(r'^(?P<school_type>[\w,]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        MonthMenuView.as_view(), name='food_menu_month'),

    url(r'^(?P<school_type>[\w,]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        DayMenuView.as_view(), name='food_menu_day'),

    url(r'^by-dish/(?P<dish_slug>[^/]+)/$',
        MealListView.as_view(),
        name='food_meals_list',
    ),

    url(r'^dish/(?P<slug>[^/]*)/$', 
        DishDetailView.as_view(), 
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
