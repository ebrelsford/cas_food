from django.contrib import admin

from models import Dish, Meal

class DishAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

class MealAdmin(admin.ModelAdmin):
    list_display = ('date', 'school_type')

admin.site.register(Dish, DishAdmin)
admin.site.register(Meal, MealAdmin)
