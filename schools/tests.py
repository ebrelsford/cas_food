import json

from django.core.urlresolvers import reverse
from django.db.models import Max
from django.test import TestCase

from schools.models import School

class SchoolsViewsTestCase(TestCase):
    fixtures = ['schools_test.json',]

    def _get_school(self):
        return School.objects.all()[0]

    #
    # map
    #

    def test_map_loads(self):
        response = self.client.get(reverse('schools.views.map'))
        self.assertEqual(response.status_code, 200)

    #
    # details
    #

    def test_details_existing_school(self):
        school = self._get_school()
        response = self.client.get(reverse('schools.views.details', kwargs={
            'school_slug': school.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_details_nonexisting_school(self):
        response = self.client.get(reverse('schools.views.details', kwargs={
            'school_slug': 'THIS COULD NOT POSSIBLY BE A SCHOOL NAME',
        }))
        self.assertEqual(response.status_code, 404)

    #
    # as_geojson successes
    #

    def test_as_geojson_existing_id(self):
        school = self._get_school()
        response = self.client.get('%s?id=%d' % 
                                   (reverse('schools.views.as_geojson'), school.id))
        self.assertEqual(response.status_code, 200)

    def test_as_geojson_existing_type(self):
        school = self._get_school()
        response = self.client.get(
            '%s?types=%s' % (reverse('schools.views.as_geojson'), school.type)
        )
        self.assertEqual(response.status_code, 200)

    def test_as_geojson_existing_borough(self):
        school = self._get_school()
        response = self.client.get(
            '%s?boroughs=%s' % (reverse('schools.views.as_geojson'), school.borough)
        )
        self.assertEqual(response.status_code, 200)

    #
    # as_geojson empty responses
    #

    def _assert_as_geojson_empty_response(self, response):
        self.assertEqual(response.status_code, 200)
        features = json.loads(response.content)['features']
        self.assertEqual(len(features), 0)

    def test_as_geojson_nonexisting_id(self):
        id = School.objects.aggregate(max_id=Max('id'))['max_id'] + 1
        response = self.client.get('%s?id=%d' % 
                                   (reverse('schools.views.as_geojson'), id))
        self._assert_as_geojson_empty_response(response)

    def test_as_geojson_nonexisting_type(self):
        type = 'THIS COULD NOT POSSIBLY BE A TYPE OF SCHOOL'
        response = self.client.get(
            '%s?types=%s' % (reverse('schools.views.as_geojson'), type)
        )
        self._assert_as_geojson_empty_response(response)

    def test_as_geojson_nonexisting_borough(self):
        borough = 'THIS COULD NOT POSSIBLY BE A BOROUGH'
        response = self.client.get(
            '%s?boroughs=%s' % (reverse('schools.views.as_geojson'), borough)
        )
        self._assert_as_geojson_empty_response(response)

    #
    # notes
    #

    def test_notes_list_existing_school(self):
        school = self._get_school()
        response = self.client.get(reverse('schools_notes_list', kwargs={
            'school_slug': school.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_notes_list_nonexisting_school(self):
        response = self.client.get(reverse('schools_notes_list', kwargs={
            'school_slug': 'THIS COULD NOT POSSIBLY BE A SCHOOL NAME',
        }))
        self.assertEqual(response.status_code, 404)

    #
    # meals
    #

    def test_meals_list_existing_school(self):
        school = self._get_school()
        response = self.client.get(reverse('schools_meals_list', kwargs={
            'school_slug': school.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_meals_list_nonexisting_school(self):
        response = self.client.get(reverse('schools_meals_list', kwargs={
            'school_slug': 'THIS COULD NOT POSSIBLY BE A SCHOOL NAME',
        }))
        self.assertEqual(response.status_code, 404)
