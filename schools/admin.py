from django.contrib import admin

from models import GardenToCafe, School

class SchoolAdmin(admin.ModelAdmin):
    search_fields = ('name', 'address',)
    list_display = ('name', 'address', 'city', 'borough', 'type', 'grades', 'has_content',)
    list_filter = ('city', 'borough', 'type', 'participates_in_wellness_in_the_schools', 'participates_in_garden_to_cafe',)

class GardenToCafeAdmin(admin.ModelAdmin):
    search_fields = ('school',)
    list_display = ('school', 'organization',)

admin.site.register(School, SchoolAdmin)
admin.site.register(GardenToCafe, GardenToCafeAdmin)
