from datetime import date

from food.models import Meal

def todays_menu(request):
    """
    Add today's elementary meals to the context, for use in the sidebar.
    """
    # TODO cache?
    return {
        'todays_menu': Meal.objects.filter(school_type='elementary',
                                           date=date.today()),
    }
