from datetime import date
import json

from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase

from food.models import Dish, Meal, Ingredient, Nutrient

class FoodViewsTestCase(TestCase):
    fixtures = [
        'auth_test.json',
        'food_test.json',
    ]

    def _get_meal(self):
        return Meal.objects.all()[0]

    def _get_dish(self):
        return Dish.objects.all()[0]

    def _add_permissions(self, username):
        u = User.objects.get(username=username)
        permission = Permission.objects.get(codename='change_dish')
        u.user_permissions.add(permission)
        u.save()


    def _login(self):
        self._add_permissions('test')
        success = self.client.login(username='test', password='test')

    #
    # menu
    #

    def test_menu_redirect(self):
        response = self.client.get(reverse('food.views.menu'))
        self.assertEqual(response.status_code, 302)

    #
    # MonthMenuView
    #

    def test_month_menu_loads(self):
        today = date.today()
        response = self.client.get(reverse('food_menu_month', kwargs={
            'school_type': self._get_meal().school_type,
            'year': today.year,
            'month': today.month,
        }))
        self.assertEqual(response.status_code, 200)

    def test_month_menu_bad_year(self):
        today = date.today()
        self.assertRaises(NoReverseMatch, lambda: reverse('food_menu_month', kwargs={
            'school_type': self._get_meal().school_type,
            'year': 123456,
            'month': today.month,
        }))

    def test_month_menu_bad_month(self):
        today = date.today()
        self.assertRaises(NoReverseMatch, lambda: reverse('food_menu_month', kwargs={
            'school_type': self._get_meal().school_type,
            'year': today.year,
            'month': 1234,
        }))

    #
    # DayMenuView
    #

    def test_day_menu_loads(self):
        today = date.today()
        response = self.client.get(reverse('food_menu_day', kwargs={
            'school_type': self._get_meal().school_type,
            'year': today.year,
            'month': today.month,
            'day': today.day,
        }))
        self.assertEqual(response.status_code, 200)

    def test_day_menu_bad_year(self):
        today = date.today()
        self.assertRaises(NoReverseMatch, lambda: reverse('food_menu_day', kwargs={
            'school_type': self._get_meal().school_type,
            'year': 123456,
            'month': today.month,
            'day': today.day,
        }))

    def test_day_menu_bad_month(self):
        today = date.today()
        self.assertRaises(NoReverseMatch, lambda: reverse('food_menu_day', kwargs={
            'school_type': self._get_meal().school_type,
            'year': today.year,
            'month': 1234,
            'day': today.day,
        }))

    def test_day_menu_bad_day(self):
        today = date.today()
        self.assertRaises(NoReverseMatch, lambda: reverse('food_menu_day', kwargs={
            'school_type': self._get_meal().school_type,
            'year': today.year,
            'month': today.month,
            'day': 1234,
        }))

    #
    # food_dish_detail
    #

    def test_dish_detail_existing_dish(self):
        response = self.client.get(reverse('food_dish_detail', kwargs={
            'slug': self._get_dish().slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_dish_detail_nonexisting_dish(self):
        response = self.client.get(reverse('food_dish_detail', kwargs={
            'slug': 'THIS COULD NOT POSSIBLY BE A DISH SLUG',
        }))
        self.assertEqual(response.status_code, 404)

    #
    # add_or_get_ingredient
    #

    def test_add_or_get_ingredient_without_login(self):
        response = self.client.get(
            reverse('food.views.add_or_get_ingredient', kwargs={
                'name': 'PROBABLY NOT AN INGREDIENT NAME',
            })
        )
        self.assertEqual(response.status_code, 302)

    def test_add_or_get_ingredient_existing_ingredient(self):
        self._login()
        ingredient = Ingredient.objects.all()[0]
        response = self.client.get(
            reverse('food.views.add_or_get_ingredient', kwargs={
                'name': ingredient.name,
            })
        )
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)
        self.assertEqual(response_content['id'], ingredient.id)
        self.assertFalse(response_content['created'])

    def test_add_or_get_ingredient_nonexisting_ingredient(self):
        self._login()
        ingredient_name = 'RIDICULOUS NAME FOR AN INGREDIENT'
        response = self.client.get(
            reverse('food.views.add_or_get_ingredient', kwargs={
                'name': ingredient_name,
            })
        )
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)

        self.assertTrue(response_content['created'])
        ingredient = Ingredient.objects.get(id=response_content['id'])
        self.assertEqual(ingredient.name.lower(), ingredient_name.lower())

    #
    # add_or_get_nutrient
    #

    def test_add_or_get_nutrient_without_login(self):
        response = self.client.get(
            reverse('food.views.add_or_get_nutrient', kwargs={
                'name': 'PROBABLY NOT AN NUTRIIENT NAME',
            })
        )
        self.assertEqual(response.status_code, 302)

    def test_add_or_get_nutrient_existing_nutrient(self):
        self._login()
        nutrient = Nutrient.objects.all()[0]
        response = self.client.get(
            reverse('food.views.add_or_get_nutrient', kwargs={
                'name': nutrient.name,
            })
        )
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)
        self.assertEqual(response_content['id'], nutrient.id)
        self.assertFalse(response_content['created'])

    def test_add_or_get_nutrient_nonexisting_nutrient(self):
        self._login()
        nutrient_name = 'RIDICULOUS NAME FOR AN INGREDIENT'
        response = self.client.get(
            reverse('food.views.add_or_get_nutrient', kwargs={
                'name': nutrient_name,
            })
        )
        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content)

        self.assertTrue(response_content['created'])
        nutrient = Nutrient.objects.get(id=response_content['id'])
        self.assertEqual(nutrient.name.lower(), nutrient_name.lower())
