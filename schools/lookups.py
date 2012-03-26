from selectable.base import ModelLookup
from selectable.registry import registry

from schools.models import School

class SchoolLookup(ModelLookup):
    filters = {
        'borough__in': ('Brooklyn', 'Manhattan',),
        'type__in': ('Elementary',),
    }
    model = School
    search_fields = ('name__icontains', 'address__icontains',)

    def get_item_label(self, item):
        return "%s (%s)" % (item.name, item.borough)

    def get_item_value(self, item):
        return "%s (%s)" % (item.name, item.borough)

    def get_item_id(self, item):
        return item.id

registry.register(SchoolLookup)
