from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from models import Callout, Dish, DishIngredient, Ingredient, Meal, Nutrient, NutritionFact

class CalloutAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_type',)
    list_filter = ('school_type',)
    search_fields = ('name',)
    ordering = ('name',)

class DishIngredientAdmin(admin.ModelAdmin):
    search_fields = ('dish', 'ingredient',)
    list_display = ('dish', 'ingredient', 'order',)

class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

class NutrientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

class NutritionFactAdmin(admin.ModelAdmin):
    list_display = ('dish', 'nutrient',)
    list_filter = ('dish__school_type',)
    ordering = ('dish__name', 'nutrient',)
    search_fields = ('dish__name', 'nutrient__name',)

class MealAdminForm(forms.ModelForm):
    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all().order_by('name'),
        widget=FilteredSelectMultiple('dishes', is_stacked=False),
    )

class MealAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    form = MealAdminForm
    list_display = ('date', 'school_type',)
    list_filter = ('date', 'school_type',)
    ordering = ('date', 'school_type',)

admin.site.register(Callout, CalloutAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(DishIngredient, DishIngredientAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Nutrient, NutrientAdmin)
admin.site.register(NutritionFact, NutritionFactAdmin)
