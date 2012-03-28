from django.contrib import admin

from models import Entry

class EntryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'text',)
    prepopulated_fields = {
        'slug': ('title',),
    }

admin.site.register(Entry, EntryAdmin)
