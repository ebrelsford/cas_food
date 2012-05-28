from django.core.urlresolvers import reverse
from django.test import TestCase

class GlossaryViewsTestCase(TestCase):
    fixtures = [
        'connect_test.json',
    ]

    def test_index_loads(self):
        response = self.client.get(reverse('connect_index'))
        self.assertEqual(response.status_code, 200)

    def test_video_list_loads(self):
        response = self.client.get(reverse('connect_video_list'))
        self.assertEqual(response.status_code, 200)

    def test_twitterfeed_list_loads(self):
        response = self.client.get(reverse('connect_twitterfeed_list'))
        self.assertEqual(response.status_code, 200)
