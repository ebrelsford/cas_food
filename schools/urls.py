from django.conf.urls.defaults import patterns, url

from schools.views import AddOrganizerView, DeleteOrganizerView, EditOrganizerView, SchoolNoteListView, MealListView

urlpatterns = patterns('',
    url(r'^geojson', 'schools.views.as_geojson'),
    url(r'^(?P<school_slug>[^/]+)/$', 'schools.views.details'),

    url(r'^(?P<school_slug>[^/]+)/comments/$', SchoolNoteListView.as_view(),
        name='schools_notes_list'
    ),

    url(r'^(?P<school_slug>[^/]+)/meals/', MealListView.as_view(),
        name='schools_meals_list'
    ),

    url(r'^(?P<school_slug>[^/]+)/comments/add/$', 'schools.views.add_note'),

    url(r'^(?P<school_slug>[^/]+)/organizers/add/$',
        AddOrganizerView.as_view(), 
        name='schools_add_organizer'
    ),

    url(r'^(?P<school_slug>[^/]+)/organizers/(?P<pk>\d+)/edit/$',
        EditOrganizerView.as_view(), 
        name='schools_edit_organizer'
    ),

    url(r'^(?P<school_slug>[^/]+)/organizers/(?P<pk>\d+)/delete/$',
        DeleteOrganizerView.as_view(), 
        name='schools_delete_organizer'
    ),
)
