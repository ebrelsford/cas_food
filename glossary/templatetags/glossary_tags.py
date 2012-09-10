from django import template
from django.utils.safestring import mark_safe

from glossary.util import link_to_glossary

register = template.Library()

@register.filter(needs_autoescape=True)
def add_glossary_links(text, arg=None, autoescape=None):
    """
    Add links to glossary entries where appropriate.
 
    If an entry's text is in the glossary, link it.

    If arg is 'direct', link directly to the glossary entry, else link to the 
    entry on the glossary list page.
    """
    text = link_to_glossary(
        text,
        direct=(arg == 'direct'),
        autoescape=autoescape,
    )

    return mark_safe(text)
