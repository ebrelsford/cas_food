from django.core.urlresolvers import reverse
from django.test import TestCase

class GlossaryViewsTestCase(TestCase):
    fixtures = [
        'auth_test.json',
        'flatpages_test.json',
        'pages_test.json',
    ]

    def test_update_not_logged_in(self):
        response = self.client.get(reverse('pages_flatpage_update',
            kwargs={
                'pk': 1, 
            },
        ))

        # should redirect to log in page
        self.assertEqual(response.status_code, 302)

    def test_update_not_logged_in_nonexistent_page(self):
        response = self.client.get(reverse('pages_flatpage_update',
            kwargs={
                'pk': 10000, 
            },
        ))

        # should still redirect to log in page
        self.assertEqual(response.status_code, 302)

    def test_update_logged_in_without_permission(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('pages_flatpage_update',
            kwargs={
                'pk': 10000, 
            },
        ))

        # should still redirect to log in page
        self.assertEqual(response.status_code, 302)

    def test_update_logged_in_with_permission(self):
        self.client.login(username='superuser', password='test')
        response = self.client.get(reverse('pages_flatpage_update',
            kwargs={
                'pk': 1, 
            },
        ))

        self.assertEqual(response.status_code, 200)
