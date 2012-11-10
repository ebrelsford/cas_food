from datetime import date

from food.models import Meal

def todays_menu(request):
    """
    Add today's elementary meals to the context, for use in the sidebar.
    """
    meals_today = Meal.objects.filter(date=date.today())
    return {
        'todays_menu': meals_today.filter(
            school_type='elementary',
        ),
        'todays_menu_elementary_alternative': meals_today.filter(
            school_type='elementary_alternative',
        ),
    }
