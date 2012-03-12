#!/usr/bin/python
# -*- coding: latin-1 -*-

from datetime import date, datetime
import re

from food.models import Meal, Dish

date_pattern = re.compile(r'^(.*) (\d{4})$')
day_of_month_pattern = re.compile(r'^(\d+)$')
meal_name_pattern = re.compile(r'^[A-Z’ ]+$', flags=re.UNICODE)
dish_name_pattern = re.compile(r'^-?(?:with )?(?:OR a )?(.*?)(?: OR)?\W*$')

def load_menu(filename, school_type):
    menu = open(filename, 'r').readlines()

    month = None
    year = None
    current_day = None
    current_meal = None

    for line in menu:
        line = line.strip()
        line = re.sub(r'\s+', ' ', line)

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
            dish_name = dish_name_match.group(1).lower()
            dish = Dish.objects.filter(name=dish_name)
            if not dish:
                dish = Dish(name=dish_name)
                dish.save()
            else:
                dish = dish[0]
            current_meal.dishes.add(dish)
            current_meal.save()
            print 'dish name (%s)' % dish_name
