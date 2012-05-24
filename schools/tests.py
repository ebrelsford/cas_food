from django.test.client import Client
from django.utils import unittest

class SchoolsViewsTestCase(unittest.TestCase):

    def test_map_loads(self):
        c = Client()
        response = c.get('/map/')
        self.assertEqual(response.status_code, 200)
