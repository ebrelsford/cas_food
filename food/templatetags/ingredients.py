from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from glossary.models import Entry

register = template.Library()

@register.filter(needs_autoescape=True)
def ingredient_list(dish, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    entries = Entry.objects.all()
    entries_dict = dict(map(lambda e: (e.title.lower(), e), entries))

    ingredients = [di.ingredient.name for di in dish.get_dishingredients()]
    if not ingredients:
        return mark_safe("We don't know yet.")

    ingredient_list = ', '.join(ingredients)

    for entry in entries_dict.keys():
        if entry in ingredient_list:
            ingredient_list = ingredient_list.replace(
                entry, 
                '<a href="%s">%s</a>' % (
                    esc(entries_dict[entry].get_absolute_url()), 
                    esc(entry)
                )
            )
    
    return mark_safe(ingredient_list)
