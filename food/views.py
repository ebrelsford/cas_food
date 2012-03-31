from datetime import date

from django.views.generic import MonthArchiveView, DayArchiveView

from mobile.shortcuts import get_template
from models import Meal

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
