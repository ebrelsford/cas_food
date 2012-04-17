from django import forms

from models import Dish, Ingredient

class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all().order_by('name'))

    class Meta:
        exclude = ('name', 'slug',)
        model = Dish
