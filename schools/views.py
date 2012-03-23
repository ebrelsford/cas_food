import geojson

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext

from cas_food.shortcuts import render_to_response
from models import School

def index(request):
    return render_to_response("schools/index.html", {}, context_instance=RequestContext(request))

def map(request):
    return render_to_response("schools/map.html", {}, context_instance=RequestContext(request))

def details(request, id=None):
    school = get_object_or_404(School, id=id)
    pictures = list(reversed(school.picture_set.order_by('-added').all()[:3]))
    return render_to_response("schools/details.html", {
        'school': school,
        'notes': school.note_set.order_by('added').all(),
        'pictures': pictures,
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
