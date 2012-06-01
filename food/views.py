from datetime import date
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, MonthArchiveView, DayArchiveView

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

        school_types = self.kwargs.get('school_type', '').split(',')
        context['school_types'] = school_types

        school_types_display = ', '.join(self.school_types_verbose[t] for t in school_types)
        context['school_types_display'] = school_types_display

        context['has_multiple_school_types'] = len(school_types) > 1
        return context

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
