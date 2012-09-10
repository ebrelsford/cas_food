from django.conf.urls.defaults import patterns, url

from schools import views

urlpatterns = patterns('',
    url(r'^geojson', 'schools.views.as_geojson'),

    url(r'^find-your-school/$', 'schools.views.map'),

    url(r'^by-borough/$', 
        views.FindSchoolByBoroughView.as_view(),
        name='schools_schools_byborough',
    ),

    url(r'^by-borough/(?P<borough>[^/]+)/$', 
        views.SchoolListView.as_view(),
        name='schools_schools_list',
    ),

    url(r'^(?P<school_slug>[^/]+)/$', 'schools.views.details'),

    url(r'^(?P<school_slug>[^/]+)/comments/$', 
        views.SchoolNoteListView.as_view(),
        name='schools_notes_list',
    ),

    url(r'^(?P<school_slug>[^/]+)/meals/', 
        views.MealListView.as_view(),
        name='schools_meals_list',
    ),

    url(r'^(?P<school_slug>[^/]+)/comments/add/$', 'schools.views.add_note'),

    url(r'^(?P<school_slug>[^/]+)/organizers/add/$',
        views.AddOrganizerView.as_view(), 
        name='schools_add_organizer'
    ),

    url(r'^(?P<school_slug>[^/]+)/organizers/(?P<pk>\d+)/edit/$',
        views.EditOrganizerView.as_view(), 
        name='schools_edit_organizer'
    ),

    url(r'^(?P<school_slug>[^/]+)/organizers/(?P<pk>\d+)/delete/$',
        views.DeleteOrganizerView.as_view(), 
        name='schools_delete_organizer'
    ),
)
