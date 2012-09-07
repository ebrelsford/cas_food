from alias.models import Alias

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
        add_alias(dish, duplicate_dish.name)
        for meal in duplicate_dish.meal_set.all():
            meal.dishes.remove(duplicate_dish)
            meal.dishes.add(dish)
            meal.save()

        # NB: assumes we can safely delete DishIngredients on duplicate
        duplicate_dish.delete()
