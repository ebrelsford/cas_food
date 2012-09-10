from django.core.urlresolvers import reverse
from django.utils.html import conditional_escape

from glossary.models import Entry

def link_to_glossary(text, direct=False, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    entries = Entry.objects.all()
    entries_dict = dict(map(lambda e: (e.title.lower(), e), entries))

    for entry_name in entries_dict.keys():
        if entry_name in text:
            entry_url = get_entry_url(entries_dict[entry_name], direct=direct)
            text = text.replace(
                entry_name, 
                '<a href="%s">%s</a>' % (esc(entry_url), esc(entry_name))
            )
    return text

def get_entry_url(entry, direct=False):
    if not direct:
        return reverse('glossary_list') + '#' + entry.slug
    else:
        return entry.get_absolute_url()
