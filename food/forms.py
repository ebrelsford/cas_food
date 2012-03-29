from django import forms

from models import Dish

class DishForm(forms.ModelForm):
    # TODO implement
    class Meta:
        model = Dish
