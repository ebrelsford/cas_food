from django.contrib import admin

from organize.models import Organizer

class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Organizer, OrganizerAdmin)
