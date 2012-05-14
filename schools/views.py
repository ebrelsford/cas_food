import geojson

from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from accounts.models import UserProfile
from content.forms import NoteForm
from feedback.forms import FeedbackResponseForm
from forms import SchoolSearchForm
from generic.views import LoginRequiredMixin, PermissionRequiredMixin
from models import School
from organize.forms import AddOrganizerForm, EditOrganizerForm
from organize.models import Organizer

def index(request):
    return render_to_response("schools/map.html", {
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

def _is_organizing(school, user):
    if user.is_authenticated():
        return school.organizers.filter(added_by=user).count() > 0
    return False

def _get_meals(school, index=0, count=3, user_id=None):
    meals = school.tray_set.all().annotate(total_points=Sum('rating__points'),
                                           total_count=Count('rating__id')).extra(
        select={
            'user_rated': "SELECT COUNT(*)=1 FROM tray_rating WHERE tray_rating.tray_id=tray_tray.id AND tray_rating.added_by_id=%s",
        },
        select_params=(user_id,),
    ).order_by('date')

    meal_count = meals.count()
    if meal_count > count:
        if index < 0:
            return meals.none()
        return meals[index:index + count]
    return meals

def details(request, school_slug=None):
    school = get_object_or_404(School, slug=school_slug)
    notes = school.notes.order_by('added').all()
    notes_to_display = 10

    return render_to_response("schools/details.html", {
        'school': school,
        'notes': notes[:notes_to_display],
        'more_notes': notes.count() > notes_to_display,
        'meals_count': school.tray_set.count(),
        'principals': school.contact_set.filter(type='principal'),
        'is_following': _is_following(school, request.user),
        'is_organizing': _is_organizing(school, request.user),
        'quiz_form': FeedbackResponseForm(initial={
            'added_by': request.user,
            'school': school,
        }),
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

class SchoolNoteListView(ListView):
    template_name = 'schools/note_list.html'

    def get_queryset(self):
        self.school = get_object_or_404(School,
                                        slug=self.kwargs['school_slug'])
        return self.school.notes.all()

    def get_context_data(self, **kwargs):
        context = super(SchoolNoteListView, self).get_context_data(**kwargs)
        context['school'] = self.school
        return context

class MealListView(ListView):
    default_count = 3
    default_index = 0

    def get_queryset(self):
        self.count = int(self.request.GET.get('count', self.default_count))
        self.index = int(self.request.GET.get('index', self.default_index))
        self.school = get_object_or_404(School,
                                        slug=self.kwargs['school_slug'])
        return _get_meals(self.school, index=self.index, count=self.count, 
                          user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(MealListView, self).get_context_data(**kwargs)
        context['school'] = self.school
        context['has_next'] = False
        context['has_previous'] = False
        return context

class SchoolOrganizerMixin(LoginRequiredMixin, FormMixin):
    model = Organizer

    def _get_school(self):
        """Get the school associated with this view."""
        try:
            return self.school
        except:
            self.school = get_object_or_404(School, slug=self.kwargs['school_slug'])
            return self.school

    def get_context_data(self, **kwargs):
        context = super(SchoolOrganizerMixin, self).get_context_data(**kwargs)
        context['school'] = self._get_school()
        return context

    def get_success_url(self):
        return reverse('schools.views.details', kwargs={
            'school_slug': self._get_school().slug,
        })

class AddOrganizerView(SchoolOrganizerMixin, PermissionRequiredMixin, CreateView):
    form_class = AddOrganizerForm
    permission = 'schools.add_organizer'
    template_name = 'schools/organizer_add.html'
    
    def get_form_kwargs(self):
        """Add school to form kwargs."""
        kwargs = super(AddOrganizerView, self).get_form_kwargs()
        kwargs['object'] = self._get_school()
        kwargs['initial']['added_by'] = self.request.user
        return kwargs

class EditOrganizerView(SchoolOrganizerMixin, PermissionRequiredMixin, UpdateView):
    form_class = EditOrganizerForm
    model = Organizer
    permission = 'schools.change_organizer'
    template_name = 'schools/organizer_edit.html'
    
    def get_form_kwargs(self):
        """Add school to form kwargs."""
        kwargs = super(EditOrganizerView, self).get_form_kwargs()
        kwargs['object'] = self._get_school()
        kwargs['initial']['updated_by'] = self.request.user
        return kwargs

class DeleteOrganizerView(SchoolOrganizerMixin, PermissionRequiredMixin, DeleteView):
    model = Organizer
    permission = 'schools.delete_organizer'
    template_name = 'schools/organizer_confirm_delete.html'
