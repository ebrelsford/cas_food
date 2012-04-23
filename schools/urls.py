from django.conf.urls.defaults import patterns, url

from schools.views import SchoolNoteListView, MealListView

urlpatterns = patterns('',
    url(r'^geojson', 'schools.views.as_geojson'),
    url(r'^(?P<school_slug>[^/]+)/$', 'schools.views.details'),

    url(r'^(?P<school_slug>[^/]+)/comments/$', SchoolNoteListView.as_view(),
        name='schools_notes_list'
    ),

    url(r'^(?P<school_slug>[^/]+)/mealsjson/', MealListView.as_view(),
        name='schools_json_meals_list'
    ),

    url(r'^(?P<school_slug>[^/]+)/comments/add/$', 'schools.views.add_note'),
)
