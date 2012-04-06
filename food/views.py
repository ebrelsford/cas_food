from datetime import date

from django.core.urlresolvers import reverse
from django.views.generic import CreateView, MonthArchiveView, DayArchiveView

from content.forms import PictureForm
from mobile.shortcuts import get_template
from models import Dish, Meal

def menu(request):
    today = date.today()
    return MonthMenuView.as_view()(request, year=str(today.year), month=str(today.month), school_type='elementary').render()

class MonthMenuView(MonthArchiveView):
    allow_empty = True
    allow_future = True
    date_field = 'date'
    month_format='%m'

    def get_queryset(self):
        self.template_name = get_template('food/meal_archive_month.html', self.request)
        return Meal.objects.filter(school_type=self.kwargs['school_type'])

    def get_context_data(self, **kwargs):
        context = super(MonthMenuView, self).get_context_data(**kwargs)
        context['school_type'] = self.kwargs['school_type']
        return context

class DayMenuView(DayArchiveView):
    allow_empty = True
    allow_future = True
    date_field = 'date'
    month_format='%m'

    def get_queryset(self):
        self.template_name = get_template('food/meal_archive_day.html', self.request)
        return Meal.objects.filter(school_type=self.kwargs['school_type'])

    def get_context_data(self, **kwargs):
        context = super(DayMenuView, self).get_context_data(**kwargs)
        context['school_type'] = self.kwargs['school_type']
        return context

class DishAddPictureView(CreateView):
    form_class = PictureForm
    template_name = 'screen/food/dish_add_picture_form.html'
    
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
