from django.contrib import admin

from models import Entry

class EntryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'text', 'added', 'added_by',)
    ordering = ('title',)
    list_filter = ('added', 'added_by',)
    date_hierarchy = 'added'

    readonly_fields = ('added', 'updated',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'text',),
        }),
        ('Audit', {
            'fields': (('added', 'added_by',), ('updated', 'updated_by',),),
        }),
    )
    prepopulated_fields = {
        'slug': ('title',),
    }

admin.site.register(Entry, EntryAdmin)
