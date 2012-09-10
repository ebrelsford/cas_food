from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
def ingredient_list(dish, arg=None, autoescape=None):
    """
    Display the ingredients list for this dish. 
    
    If ingredient (or part of an ingredient) is in the glossary, link to the 
    glossary entry. If arg is 'direct', link directly to the glossary entry,
    else link to the entry on the glossary list page.
    """
    ingredients = [di.ingredient.name for di in dish.get_dishingredients()]
    if not ingredients:
        return mark_safe("We don't know yet.")

    ingredient_list = ', '.join(ingredients)
    return ingredient_list
