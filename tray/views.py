import json

from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from content.forms import NoteForm
from schools.models import School
from forms import TrayForm
from models import Tray, Rating

@login_required
@permission_required('tray.add_tray')
def add(request, school_slug=None):
    initial = {
        'added_by': request.user,
        'school': get_object_or_404(School, slug=school_slug)
    }

    if request.method == 'POST':
        form = TrayForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('schools.views.details',
                            school_slug=initial['school'].slug)
    else:
        form = TrayForm(initial=initial)

    return render_to_response('tray/add.html', {
        'school': initial['school'],
        'form': form,
    }, context_instance=RequestContext(request))

def details(request, school_slug=None, tray_id=None):
    """Details for the given tray"""
    try:
        trays = Tray.objects.filter(school__slug=school_slug, id=tray_id)
        trays = trays.annotate(total_points=Sum('rating__points'),
                               total_count=Count('rating__id'))
        tray = trays.extra(
            select={
                'user_rated': ("SELECT COUNT(*)=1 "
                               "FROM tray_rating "
                               "WHERE tray_rating.tray_id=tray_tray.id "
                               "AND tray_rating.added_by_id=%s"),
            },
            select_params=(request.user.id,),
        )[0]
    except:
        raise Http404

    comment_form = NoteForm(object=tray, initial={ 'added_by': request.user })

    return render_to_response('tray/details.html', {
        'school': tray.school,
        'comment_form': comment_form,
        'tray': tray,
    }, context_instance=RequestContext(request))

@login_required
@permission_required('content.add_note')
def add_comment(request, school_slug=None, tray_id=None):
    tray = get_object_or_404(Tray, school__slug=school_slug, id=tray_id)
    if request.method == "POST":
        comment_form = NoteForm(request.POST, object=tray,
                                initial={ 'added_by': request.user })
        if comment_form.is_valid():
            comment_form.save()
            return redirect('tray.views.details', school_slug=school_slug,
                            tray_id=tray_id)
    else:
        return HttpResponseNotAllowed(['POST',])

def _add_rating(tray, user, points):
    """
    Add a rating to a tray for a user, deleting other ratings by that user 
    first.
    """
    Rating.objects.filter(tray=tray, added_by=user).delete()
    rating = Rating(tray=tray, points=points, added_by=user)
    rating.save()

def rate(request, school_slug=None, tray_id=None):
    """Rate a tray (tray_id) posted on a school (school_slug)."""
    status = 'OK'
    try:
        points = request.GET.get('points')
        tray = Tray.objects.get(school__slug=school_slug, id=tray_id)
        _add_rating(tray, request.user, points)
    except:
        status = 'failure'

    ratings = Rating.objects.filter(tray=tray)

    return HttpResponse(mimetype='application/json', content=json.dumps({
        'sum': ratings.aggregate(sum=Sum('points'))['sum'],
        'count': ratings.count(),
        'status': status,
    }))
