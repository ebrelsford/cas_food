import json

from django.http import HttpResponse
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext

from cas_food.shortcuts import render_to_response
from content.forms import NoteForm
from schools.models import School
from forms import TrayForm
from models import Tray, Rating

def add(request, id=None):
    initial = {
        'added_by': request.user,
        'school': get_object_or_404(School, id=id)
    }

    if request.method == 'POST':
        form = TrayForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('schools.views.details', id=id)
    else:
        form = TrayForm(initial=initial)

    return render_to_response('tray/add.html', {
        'school': initial['school'],
        'form': form,
    }, context_instance=RequestContext(request))

def details(request, id=None, tray_id=None):
    """Details for the given tray"""
    tray = get_object_or_404(Tray, school__id=id, id=tray_id)

    if request.method == "POST":
        comment_form = NoteForm(request.POST, object=tray, initial={ 'added_by': request.user })
        if comment_form.is_valid():
            comment_form.save()
            return redirect('tray.views.details', id=id, tray_id=tray_id)
    else:
        comment_form = NoteForm(object=tray, initial={ 'added_by': request.user })

    return render_to_response('tray/details.html', {
        'school': tray.school,
        'comment_form': comment_form,
        'tray': tray,
    }, context_instance=RequestContext(request))

def comment(request, id=None, tray_id=None):
    """Post a comment on this tray"""

def _add_rating(tray, user, points):
    """Add a rating to a tray for a user, deleting other ratings by that user first."""
    Rating.objects.filter(tray=tray, added_by=user).delete()
    rating = Rating(tray=tray, points=points, added_by=user)
    rating.save()

def _get_average_points(tray):
    """Get the average points for this tray."""
    return Rating.objects.filter(tray=tray).aggregate(average_points=Avg('points'))['average_points']

def rate(request, id=None, tray_id=None):
    """Rate a tray (tray_id) posted on a school (id)."""
    status = 'OK'
    try:
        points = request.GET.get('points')
        tray = Tray.objects.get(school__id=id, id=tray_id)
        _add_rating(tray, request.user, points)
    except:
        status = 'failure'

    return HttpResponse(mimetype='application/json', content=json.dumps({
        'average': _get_average_points(tray),
        'count': Rating.objects.filter(tray=tray).count(),
        'status': status,
    }))
