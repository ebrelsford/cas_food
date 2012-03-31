import json

from django.http import HttpResponse
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext

from content.forms import NoteForm
from schools.models import School
from mobile.shortcuts import render_to_response
from forms import TrayForm
from models import Tray, Rating

def add(request, school_slug=None):
    initial = {
        'added_by': request.user,
        'school': get_object_or_404(School, slug=school_slug)
    }

    if request.method == 'POST':
        form = TrayForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('schools.views.details', school_slug=initial['school'].slug)
    else:
        form = TrayForm(initial=initial)

    return render_to_response('tray/add.html', {
        'school': initial['school'],
        'form': form,
    }, context_instance=RequestContext(request))

def details(request, school_slug=None, tray_id=None):
    """Details for the given tray"""
    tray = get_object_or_404(Tray, school__slug=school_slug, id=tray_id)

    if request.method == "POST":
        comment_form = NoteForm(request.POST, object=tray, initial={ 'added_by': request.user })
        if comment_form.is_valid():
            comment_form.save()
            return redirect('tray.views.details', school_slug=school_slug, tray_id=tray_id)
    else:
        comment_form = NoteForm(object=tray, initial={ 'added_by': request.user })

    return render_to_response('tray/details.html', {
        'school': tray.school,
        'comment_form': comment_form,
        'tray': tray,
    }, context_instance=RequestContext(request))

def _add_rating(tray, user, points):
    """Add a rating to a tray for a user, deleting other ratings by that user first."""
    Rating.objects.filter(tray=tray, added_by=user).delete()
    rating = Rating(tray=tray, points=points, added_by=user)
    rating.save()

def _get_average_points(tray):
    """Get the average points for this tray."""
    return Rating.objects.filter(tray=tray).aggregate(average_points=Avg('points'))['average_points']

def rate(request, school_slug=None, tray_id=None):
    """Rate a tray (tray_id) posted on a school (school_slug)."""
    status = 'OK'
    try:
        points = request.GET.get('points')
        tray = Tray.objects.get(school__slug=school_slug, id=tray_id)
        _add_rating(tray, request.user, points)
    except:
        status = 'failure'

    return HttpResponse(mimetype='application/json', content=json.dumps({
        'average': _get_average_points(tray),
        'count': Rating.objects.filter(tray=tray).count(),
        'status': status,
    }))
