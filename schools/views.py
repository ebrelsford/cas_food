import geojson

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext

from accounts.models import UserProfile
from content.forms import NoteForm
from forms import SchoolSearchForm
from mobile.shortcuts import render_to_response
from models import School
from tray.models import Rating

def index(request):
    return render_to_response("schools/index.html", {
        'form': SchoolSearchForm()
    }, context_instance=RequestContext(request))

def map(request):
    return render_to_response("schools/map.html", {
        'form': SchoolSearchForm()
    }, context_instance=RequestContext(request))

def _is_following(school, user):
    if user.is_authenticated():
        return UserProfile.objects.filter(schools_following=school, user=user).count() > 0
    return False

def _get_meals(request, school, count=3):
    meals = school.tray_set.all().annotate(total_points=Sum('rating__points'), total_count=Count('rating__id')).extra(
        select={
            'user_rated': "SELECT COUNT(*)=1 FROM tray_rating WHERE tray_rating.tray_id=tray_tray.id AND tray_rating.added_by_id=%s",
        },
        select_params=(request.user.id,),
    ).order_by('added')

    if meals.count() > 3:
        meals = meals[meals.count() - 3:]

    for m in meals:
        print m.user_rated
    return meals

def details(request, school_slug=None):
    school = get_object_or_404(School, slug=school_slug)
    meals = _get_meals(request, school)

    return render_to_response("schools/details.html", {
        'school': school,
        'notes': school.notes.order_by('added').all(),
        'meals': meals,
        'principals': school.contact_set.filter(type='principal'),
        'is_following': _is_following(school, request.user),
    }, context_instance=RequestContext(request))

def as_geojson(request):
    schools = _filter_schools(request).distinct()
    schools_geojson = _school_collection(schools) 
    response = HttpResponse(mimetype='application/json')
    response.write(geojson.dumps(schools_geojson))
    return response            

def _school_collection(schools):
    return geojson.FeatureCollection(features=[_school_feature(school) for school in schools])

def _school_feature(school):
    return geojson.Feature(
        school.id,
        geometry=geojson.Point(coordinates=(school.point.x, school.point.y)),
        properties={
            'name': school.name,
            'slug': school.slug,
            'address': school.address,
            'participates_in_wellness_in_the_schools': school.participates_in_wellness_in_the_schools,
            'participates_in_garden_to_cafe': school.participates_in_garden_to_cafe,
        },
    )

def _filter_schools(request):
    mapped_schools = School.objects.filter(point__isnull=False)
    schools = mapped_schools

    if 'id' in request.GET:
        return schools.filter(id=request.GET['id'], point__isnull=False)

    if 'types' in request.GET:
        school_types = request.GET['types'].split(',')
        schools = schools.filter(type__in=school_types)

    if 'boroughs' in request.GET:
        boroughs = request.GET['boroughs'].split(',')
        schools = schools.filter(borough__in=boroughs)

    return schools

@login_required
@permission_required('content.add_note')
def add_note(request, school_slug=None):
    school = get_object_or_404(School, slug=school_slug)
    return _add(request, school, NoteForm, 'Note')

def _add(request, school, form_class, type_text, is_multipart=False):
    if request.method == 'POST':
        if is_multipart:
            form = form_class(request.POST, request.FILES, object=school) 
        else:
            form = form_class(request.POST, object=school) 
        if form.is_valid():    
            form.save()        
            return redirect('schools.views.details', school_slug=school.slug)
    else:
        form = form_class(object=school, initial={
            'added_by': request.user,
        })

    return render_to_response('content/add.html', {
        'type': type_text,
        'school': school,
        'form': form,
        'is_multipart': is_multipart,
    }, context_instance=RequestContext(request))
