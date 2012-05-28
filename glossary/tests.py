from django.core.urlresolvers import reverse
from django.test import TestCase

from glossary.models import Entry

class GlossaryViewsTestCase(TestCase):
    fixtures = [
        'glossary_test.json',
    ]

    def test_entry_list(self):
        response = self.client.get(reverse('glossary_list'))
        self.assertEqual(response.status_code, 200)

    def test_entry_detail_existing_entry(self):
        entry = Entry.objects.all()[0]
        response = self.client.get(reverse('glossary_entry_detail', kwargs={
            'slug': entry.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_entry_detail_nonexisting_entry(self):
        response = self.client.get(reverse('glossary_entry_detail', kwargs={
            'slug': 'THIS-IS-NOT-AN-ENTRY-SLUG',
        }))
        self.assertEqual(response.status_code, 404)
