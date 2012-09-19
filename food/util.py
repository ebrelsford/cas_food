from alias.models import Alias
from food.models import MealDish

def add_alias(dish, alias_text):
    alias = Alias(
        aliased_object=dish,
        text=alias_text,
    )
    alias.save()
    return alias

def consolidate_dish(dish, duplicates):
    """
    Remove duplicate dishes, add aliases to the dish we're consolidating on.
    """
    for duplicate_dish in duplicates:
        alias = add_alias(dish, duplicate_dish.name)
        for meal in duplicate_dish.meal_set.all():
            # delete duplicate dish
            MealDish.objects.filter(
                dish=duplicate_dish,
                meal=meal,
            ).delete()

            # add consolidated dish, with alias
            mealdish = MealDish(
                alias=alias,
                dish=dish,
                meal=meal,
            )
            mealdish.save()

        # NB: assumes we can safely delete DishIngredients on duplicate
        duplicate_dish.delete()

# TODO consolidate dish without creating an Alias
