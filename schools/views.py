import geojson

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext

from content.forms import NoteForm
from forms import SchoolSearchForm
from mobile.shortcuts import render_to_response
from models import School

def index(request):
    return render_to_response("schools/index.html", {
        'form': SchoolSearchForm()
    }, context_instance=RequestContext(request))

def map(request):
    return render_to_response("schools/map.html", {
        'form': SchoolSearchForm()
    }, context_instance=RequestContext(request))

def details(request, school_slug=None):
    school = get_object_or_404(School, slug=school_slug)
    meals = school.tray_set.all().order_by('added')
    if meals.count() > 3:
        meals = meals[meals.count() - 3:]
    return render_to_response("schools/details.html", {
        'school': school,
        'notes': school.notes.order_by('added').all(),
        'meals': meals,
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

@permission_required('content.add_picture')
def add_meal(request, id=None):
    pass

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
