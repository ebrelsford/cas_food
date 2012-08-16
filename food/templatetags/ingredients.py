from django import template
from django.core.urlresolvers import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from glossary.models import Entry

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
    ingredient_list = _link_to_glossary(
        ingredient_list,
        direct=(arg == 'direct'),
        autoescape=autoescape,
    )

    return mark_safe(ingredient_list)

def _link_to_glossary(ingredients_text, direct=False, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    entries = Entry.objects.all()
    entries_dict = dict(map(lambda e: (e.title.lower(), e), entries))

    for entry_name in entries_dict.keys():
        if entry_name in ingredients_text:
            entry_url = _get_entry_url(entries_dict[entry_name], direct=direct)
            ingredients_text = ingredients_text.replace(
                entry_name, 
                '<a href="%s">%s</a>' % (esc(entry_url), esc(entry_name))
            )
    return ingredients_text

def _get_entry_url(entry, direct=False):
    if not direct:
        return reverse('glossary_list') + '#' + entry.slug
    else:
        return entry.get_absolute_url()
