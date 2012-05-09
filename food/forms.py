from django import forms
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import SelectMultiple

from models import Callout, Dish, Ingredient, DishIngredient

class OrderedDishIngredientChoiceIterator(ModelChoiceIterator):
    """
    ModelChoiceIterator that orders Ingredients by the DishIngredient order if
    they are associated with the given Dish. Otherwise, they are sorted by
    name.
    """
    def __init__(self, field, dish):
        self.dish = dish
        super(OrderedDishIngredientChoiceIterator, self).__init__(field)

    def __len__(self):
        return Ingredient.objects.count()

    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        
        # first return DishIngredients for this dish
        dish_ingredients = DishIngredient.objects.filter(dish=self.dish).order_by('order')
        for di in dish_ingredients:
            yield self.choice(di.ingredient)

        # now return any ingredients not in this dish
        other_ingredients = Ingredient.objects.exclude(dishingredient__in=dish_ingredients).order_by('name')
        for ingredient in other_ingredients:
            yield self.choice(ingredient)

class OrderedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    A ModelMultipleChoiceField that remembers the order of the pks submitted
    in the POST request.
    """
    def clean(self, value):
        qs = super(OrderedModelMultipleChoiceField, self).clean(value)
        return sorted(qs, key=lambda x:value.index(str(x.pk)))

class DishForm(forms.ModelForm):
    callouts = forms.ModelMultipleChoiceField(
        queryset=Callout.objects.all().order_by('name'))

    class Meta:
        exclude = ('name', 'slug',)
        model = Dish

    def __init__(self, *args, **kwargs):
        """
        Override to make an iterator for the Dish instance.
        """
        super(DishForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.fields['ingredients'] = OrderedModelMultipleChoiceField(Ingredient.objects.all())
            widget = SelectMultiple(
                choices=OrderedDishIngredientChoiceIterator(self.fields['ingredients'], kwargs['instance'])
            )
            self.fields['ingredients'].widget = widget

    def save(self, force_insert=False, force_update=False, commit=True):
        """
        Override to keep ingredients in order in database.
        """
        dish = super(DishForm, self).save(commit=False)
        
        # add ingredients in order
        ingredients = self.cleaned_data.get('ingredients', None)
        dish.ingredients.clear()
        for index, ingredient in enumerate(ingredients):
            dish_ingredient = DishIngredient(
                dish=dish,
                ingredient=ingredient,
                order=(index + 1) # save 0 for unordered ingredients
            )
            dish_ingredient.save()

        if commit:
            dish.save()
        return dish
