from django.contrib import admin

from models import School

class SchoolAdmin(admin.ModelAdmin):
    search_fields = ('name', 'address',)
    list_display = ('name', 'address', 'city', 'type', 'grades', 'has_content',)

admin.site.register(School, SchoolAdmin)
