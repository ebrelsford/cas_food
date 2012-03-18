from django.contrib import admin

from models import School

class SchoolAdmin(admin.ModelAdmin):
    search_fields = ('name', 'address',)
    list_display = ('name', 'address', 'city', 'type', 'grades', 'has_content',)
    list_filter = ('city', 'type', 'participates_in_wellness_in_the_schools',)

admin.site.register(School, SchoolAdmin)
