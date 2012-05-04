from django import forms

from models import Callout, Dish, Ingredient

class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all().order_by('name'))
    callouts = forms.ModelMultipleChoiceField(
        queryset=Callout.objects.all().order_by('name'))

    class Meta:
        exclude = ('name', 'slug',)
        model = Dish
