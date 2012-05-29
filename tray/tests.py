from django.core.urlresolvers import reverse
from django.test import TestCase

from tray.models import Tray

class TrayViewsTestCase(TestCase):
    fixtures = [
        'auth_test.json',
        'schools_test.json',
        'tray_test.json',
    ]

    def test_tray_detail_existing_tray(self):
        tray = Tray.objects.all()[0]
        response = self.client.get(reverse('tray.views.details', kwargs={
            'school_slug': tray.school.slug,
            'tray_id': tray.pk,
        }))
        self.assertEqual(response.status_code, 200)

    def test_tray_detail_nonexisting_tray(self):
        response = self.client.get(reverse('tray.views.details', kwargs={
            'school_slug': 'NONEXISTENT-SCHOOL-SLUG',
            'tray_id': 10009,
        }))
        self.assertEqual(response.status_code, 404)

# TODO test ratings:
    # a school
    # two users for ratings
