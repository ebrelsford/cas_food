from django.core.urlresolvers import reverse
from django.test import TestCase

from getinvolved.models import Post

class GetInvolvedViewsTestCase(TestCase):
    fixtures = [
        'getinvolved_test.json',
    ]

    def test_post_list(self):
        response = self.client.get(reverse('getinvolved_post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_existing_post(self):
        post = Post.objects.all()[0]
        response = self.client.get(reverse('getinvolved_post_detail', kwargs={
            'pk': post.pk,
        }))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_nonexisting_post(self):
        response = self.client.get(reverse('getinvolved_post_detail', kwargs={
            'pk': 10009,
        }))
        self.assertEqual(response.status_code, 404)

