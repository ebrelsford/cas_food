from django.contrib.contenttypes import generic
from django.contrib.flatpages.models import FlatPage

from content.models import Section

class SectionedFlatPage(FlatPage):
    """A FlatPage with sections"""
    sections = generic.GenericRelation(Section)

    def get_sections(self):
        return self.sections.all().order_by('weight')
