import json

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.test import TestCase

from tray.models import Rating, Tray

class TrayViewsTestCase(TestCase):
    fixtures = [
        'auth_test.json',
        'schools_test.json',
        'tray_test.json',
    ]

    def _get_rating(self, tray):
        rating = Rating.objects.filter(tray=tray).aggregate(sum=Sum('points'))['sum']
        return rating or 0

    def _get_tray(self):
        return Tray.objects.all()[0]

    def test_tray_detail_existing_tray(self):
        tray = self._get_tray()
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

    def test_tray_rating_not_logged_in(self):
        tray = self._get_tray()
        response = self.client.get(reverse('tray.views.rate', kwargs={
            'school_slug': tray.school.slug,
            'tray_id': tray.pk,
        }))

        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'failure')

    def _rate_tray_with_user(self, tray, points=1, username=None, password=None):
        self.client.login(username=username, password=password)

        url = reverse('tray.views.rate', kwargs={
            'school_slug': tray.school.slug,
            'tray_id': tray.pk,
        })
        return self.client.get(url + '?points=%d' % points)

    def test_tray_rating_one_user_once(self):
        tray = self._get_tray()
        points = 1
        pre_rating = self._get_rating(tray)

        response = self._rate_tray_with_user(tray, points=points,
                                             username='superuser', password='test')
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'OK')

        post_rating = self._get_rating(tray)
        self.assertEqual(post_rating, pre_rating + points)

    def test_tray_rating_one_user_twice(self):
        tray = self._get_tray()
        points = 1

        # rate once
        pre_rating = self._get_rating(tray)
        response = self._rate_tray_with_user(
            tray,
            points=points,
            username='superuser',
            password='test'
        )

        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'OK')
        post_rating = self._get_rating(tray)
        self.assertEqual(post_rating, pre_rating + points)

        # rate twice
        response_twice = self._rate_tray_with_user(
            tray,
            points=points,
            username='superuser',
            password='test'
        )
        response_twice_json = json.loads(response_twice.content)
        self.assertEqual(response_twice_json['status'], 'OK')

        post_second_rating = self._get_rating(tray)
        self.assertEqual(post_second_rating, post_rating)

    def test_tray_rating_two_users(self):
        self.client.login(username='superuser', password='test')

        tray = self._get_tray()
        points = 1

        # rate with first user
        pre_rating = self._get_rating(tray)
        response = self._rate_tray_with_user(
            tray,
            points=points,
            username='superuser',
            password='test'
        )
        response_json = json.loads(response.content)
        self.assertEqual(response_json['status'], 'OK')
        post_rating = self._get_rating(tray)
        self.assertEqual(post_rating, pre_rating + points)

        # rate with second user
        response_twice = self._rate_tray_with_user(
            tray,
            points=points,
            username='test',
            password='test'
        )
        response_twice_json = json.loads(response_twice.content)
        self.assertEqual(response_twice_json['status'], 'OK')
        post_second_rating = self._get_rating(tray)
        self.assertEqual(post_second_rating, post_rating + points)
