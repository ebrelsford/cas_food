from django import forms

from models import Dish

class DishForm(forms.ModelForm):
    # TODO implement
    class Meta:
        exclude = ('name', 'slug',)
        model = Dish
