from datetime import date
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, DayArchiveView, DetailView,\
        ListView, MonthArchiveView, UpdateView

from alias.models import Alias
from content.forms import PictureForm
from forms import DishForm
from generic.views import LoginRequiredMixin, PermissionRequiredMixin
from models import Dish, Ingredient, Meal, Nutrient, NutritionFact

@login_required
@permission_required('food.change_dish')
def add_or_get_ingredient(request, name=None):
    try:
        ingredient, created = Ingredient.objects.get_or_create(name=name.lower())
        result = {
            'id': ingredient.id,
            'created': created,
        }
    except:
        result = {
            'id': None,
            'created': False,
        }
    return HttpResponse(json.dumps(result), mimetype='application/json')

@login_required
@permission_required('food.change_dish')
def add_or_get_nutrient(request, name=None):
    try:
        nutrient, created = Nutrient.objects.get_or_create(name=name.lower())
        result = {
            'id': nutrient.id,
            'created': created,
        }
    except:
        result = {
            'id': None,
            'created': False,
        }
    return HttpResponse(json.dumps(result), mimetype='application/json')

def menu(request, school_type='elementary'):
    today = date.today()
    return redirect('food_menu_month',
        year=str(today.year),
        month=str(today.month),
        school_type=school_type
    )

def todays_menu(request, school_type='elementary'):
    today = date.today()
    return redirect('food_menu_day',
        year=str(today.year),
        month=str(today.month),
        day=str(today.day),
        school_type=school_type
    )

class MonthMenuView(MonthArchiveView):
    allow_empty = True
    allow_future = True
    date_field = 'date'
    month_format = '%m'
    template_name = 'food/meal_archive_month.html'

    school_types_verbose = {
        'elementary': 'elementary',
        'wits': 'Wellness in the Schools',
    }

    def get_queryset(self):
        school_types = self.kwargs.get('school_type', '').split(',')
        return Meal.objects.filter(school_type__in=school_types).order_by('date', 'school_type')

    def get_context_data(self, **kwargs):
        context = super(MonthMenuView, self).get_context_data(**kwargs)
        context['school_type'] = self.kwargs['school_type']

        school_types = filter(lambda t: t in self.school_types_verbose.keys(),
            self.kwargs.get('school_type', '').split(',')
        )
        if not school_types:
            raise Http404
        context['school_types'] = school_types

        school_types_display = ', '.join(self.school_types_verbose[t] for t in school_types)
        context['school_types_display'] = school_types_display

        context['has_multiple_school_types'] = len(school_types) > 1
        return context

class MealListView(ListView):
    model = Meal

    def get_context_data(self, **kwargs):
        context = super(MealListView, self).get_context_data(**kwargs)
        context['dish'] = self.dish
        return context

    def get_queryset(self):
        meals = super(MealListView, self).get_queryset()

        try:
            dish_slug = self.kwargs.get('dish_slug', None)
            self.dish = Dish.objects.get(slug=dish_slug)
            meals = meals.filter(dishes__pk=self.dish.pk)
        except:
            self.dish = None

        return meals.order_by('date')

class DayMenuView(DayArchiveView):
    allow_empty = True
    allow_future = True
    date_field = 'date'
    month_format = '%m'
    template_name = 'food/meal_archive_day.html'

    def get_queryset(self):
        school_types = self.kwargs.get('school_type', '').split(',')
        return Meal.objects.filter(school_type__in=school_types)

    def get_context_data(self, **kwargs):
        context = super(DayMenuView, self).get_context_data(**kwargs)
        context['school_type'] = self.kwargs['school_type']
        context['has_multiple_school_types'] = ',' in self.kwargs['school_type']
        return context

class DishDetailView(DetailView):
    model = Dish

    def get_context_data(self, **kwargs):
        context = super(DishDetailView, self).get_context_data(**kwargs)
        context['meal_count'] = Meal.objects.filter(
            school_type=self.object.school_type,
        ).count()
        context['aliases'] = Alias.objects.filter(
            aliased_type=ContentType.objects.get_for_model(Dish),
            aliased_object_id=self.object.pk,
        ).order_by('text')
        return context

class DishAddPictureView(LoginRequiredMixin, PermissionRequiredMixin,
                         CreateView):
    form_class = PictureForm
    template_name = 'food/dish_add_picture_form.html'
    permission = 'content.add_picture'
    
    def get_initial(self):
        """add added_by"""
        initial = super(DishAddPictureView, self).get_initial()
        initial['added_by'] = self.request.user
        return initial

    def get_form_kwargs(self):
        kwargs = super(DishAddPictureView, self).get_form_kwargs()
        self.dish = Dish.objects.get(slug=self.kwargs['slug'])
        kwargs['object'] = self.dish
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DishAddPictureView, self).get_context_data(**kwargs)
        context['dish'] = self.dish
        return context

    def get_success_url(self):
        return reverse('food_dish_detail', kwargs={ 'slug': self.dish.slug })

class DishUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = DishForm
    model = Dish
    permission = 'food.change_dish'

    def _get_nutrition_formset_factory(self):
        """Get a formset factory for this model and NutritionFact"""
        return inlineformset_factory(self.model, NutritionFact)

    def _get_nutrition_formset(self):
        """Get the NutritionFormSet"""
        try:
            # might have been added in post()
            return self.nutrition_formset
        except:
            NutritionFormSet = self._get_nutrition_formset_factory()
            return NutritionFormSet(instance=self.get_object())

    def get_context_data(self, **kwargs):
        context = super(DishUpdateView, self).get_context_data(**kwargs)
        context['nutrition_formset'] = self._get_nutrition_formset()
        return context

    def post(self, request, *args, **kwargs):
        """Get both the form and the formset, confirm that both are valid"""
        self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        NutritionFormSet = self._get_nutrition_formset_factory()
        self.nutrition_formset = NutritionFormSet(request.POST, request.FILES,
                                                  instance=self.object)

        if form.is_valid() and self.nutrition_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Save formset, then pass it up to save the form"""
        self.nutrition_formset.save()
        return super(DishUpdateView, self).form_valid(form)
