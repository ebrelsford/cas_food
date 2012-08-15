from food.models import Dish, DishIngredient, Ingredient

def load_dishes(filename, school_type):
    """
    Load dishes and their ingredients from a file of dishes followed by their
    ingredients, one per line, with dish names preceded by an *.
    """
    dishes = open(filename, 'r').readlines()

    for line in dishes:
        if line.startswith('*'):
            dish_name = line.replace('*', '').lower().strip()

            # get or create dish
            dish, created = Dish.objects.get_or_create(
                name=dish_name,
                school_type=school_type
            )
            ingredient_index = 1

            dish.ingredients.clear()
        else:
            # get ingredient
            ingredient_name = line.lower().strip()
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name
            )

            # add ingredient, in order given
            dish_ingredient = DishIngredient(
                dish=dish,
                ingredient=ingredient,
                order=ingredient_index
            )
            dish_ingredient.save()
            ingredient_index += 1
