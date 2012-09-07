#!/usr/bin/python
# -*- coding: latin-1 -*-

from datetime import date, datetime
from itertools import tee, izip
import re

from food.models import Meal, Dish

date_pattern = re.compile(r'^(.*) (\d{4})$')
day_of_month_pattern = re.compile(r'^(\d+)$')
meal_name_pattern = re.compile(r'^[A-Z’ ]+$', flags=re.UNICODE)
dish_name_pattern = re.compile(r'^-?(?:OR a )?(.*?)(?: OR)?\W*$')

JOINERS = ('on', 'with',)

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def _remove_non_ascii(s): 
    return "".join(i for i in s if ord(i)<128)

def _prepare_string(s):
    """
    Get a string ready to be looked at, removing extra spaces, non-ascii 
    characters.
    """
    s = s.strip()
    s = re.sub(r'\s+', ' ', s)
    s = _remove_non_ascii(s)
    return s

def load_menu(filename, school_type):
    menu = open(filename, 'r').readlines()

    month = None
    year = None
    current_day = None
    current_meal = None

    for line, next_line in _pairwise(menu):
        line = _prepare_string(line)
        next_line = _prepare_string(next_line)

        if not line:
            continue

        # <month> <year>
        date_pattern_match = date_pattern.match(line)
        if date_pattern_match:
            menu_date = datetime.strptime(line, '%B %Y')
            print menu_date
            month = menu_date.month
            year = menu_date.year
            continue

        # day of the month
        if day_of_month_pattern.match(line):
            current_day = date(year, month, int(line))
            current_meal = Meal(date=current_day, school_type=school_type)
            current_meal.save()
            print current_day
            continue

        # meal
        if meal_name_pattern.match(line):
            # TODO could combine meal name lines
            print 'meal name', line
            continue

        # dish
        dish_name_match = dish_name_pattern.match(line)
        if dish_name_match:
            dish_name = dish_name_match.group(1)

            # should have already joined this line with the previous, ignore it
            if any([line.startswith(joiner) for joiner in JOINERS]):
                continue

            # try to match with next line
            if any([next_line.startswith(joiner) for joiner in JOINERS]):
                dish_name = ' '.join((dish_name, next_line,))
            dish_name = dish_name.lower()

            try:
                # attempt to find dish, including possible aliases
                dish = Dish.objects.with_alias(dish_name).get(school_type=school_type)
            except:
                # add the dish
                dish = Dish(name=dish_name, school_type=school_type)
                dish.save()

            current_meal.dishes.add(dish)
            current_meal.save()
            print 'dish name (%s as %s)' % (dish_name, dish.name)
