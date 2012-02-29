from django.contrib import admin

from models import Dish

class DishAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

admin.site.register(Dish, DishAdmin)
