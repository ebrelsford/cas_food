from django.contrib import admin

from models import Callout, Dish, Ingredient, Meal, Nutrient, NutritionFact

class CalloutAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

class DishAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

class NutrientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

class NutritionFactAdmin(admin.ModelAdmin):
    search_fields = ('dish__name', 'nutrient__name',)
    list_display = ('dish', 'nutrient',)

class MealAdmin(admin.ModelAdmin):
    list_display = ('date', 'school_type')

admin.site.register(Callout, CalloutAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Nutrient, NutrientAdmin)
admin.site.register(NutritionFact, NutritionFactAdmin)
