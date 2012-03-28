from datetime import date

from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic.date_based import archive_day, archive_month

from cas_food.shortcuts import get_template, render_to_response
from models import Dish, Meal

def menu_month(request, school_type=None, year=None, month=None):
    month, year = int(month), int(year)
    next_month = (month % 12) + 1
    next_year = year
    if next_month == 1:
        next_year = year + 1

    previous_month = (month - 1) or 12
    previous_year = year
    if previous_month == 12:
        previous_year = year - 1

    kwargs = dict(
        allow_empty=True,
        allow_future=True,
        date_field='date',
        extra_context={ 
            'month_num': month, 
            'next_month': next_month,
            'next_year': next_year,
            'previous_month': previous_month,
            'previous_year': previous_year,
            'school_type': school_type,
            'year_num': year,
        },
        month=month,
        month_format='%m',
        queryset=Meal.objects.filter(school_type=school_type),
        template_name=get_template('food/meal_archive_month.html', request),
        year=year,
    )
    return archive_month(request, **kwargs)

def menu_day(request, school_type=None, year=None, month=None, day=None):
    kwargs = dict(
        allow_future=True,
        date_field='date',
        day=day,
        extra_context={ 'school_type': school_type },
        month=month,
        month_format='%m',
        queryset=Meal.objects.filter(school_type=school_type),
        template_name=get_template('food/meal_archive_day.html', request),
        year=year
    )
    return archive_day(request, **kwargs)

def menu(request):
    today = date.today()
    return menu_month(request, school_type='elementary', year=today.year, month=today.month)

def details(request, id=None):
    dish = get_object_or_404(Dish, id=id)
    return render_to_response('food/details.html', {
        'dish': dish,
    }, context_instance=RequestContext(request))
