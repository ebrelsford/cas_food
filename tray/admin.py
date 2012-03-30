from django.contrib import admin

from models import Tray

class TrayAdmin(admin.ModelAdmin):
    list_display = ('school', 'date', 'description', 'added_by',)
    list_filter = ('added_by', 'date',)
    ordering = ('date',)
    date_hierarchy = 'date'

    readonly_fields = ('added', 'updated',)

    fieldsets = (
        (None, {
            'fields': ('school', 'date', 'description',),
        }),
        ('Audit', {
            'fields': (('added', 'added_by',), ('updated', 'updated_by',),),
        }),
    )

admin.site.register(Tray, TrayAdmin)

