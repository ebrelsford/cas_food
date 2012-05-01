from django.contrib import admin

from models import FeedbackResponse

class FeedbackResponseAdmin(admin.ModelAdmin):
    search_fields = ('school',)
    list_display = ('school', 'added', 'added_by',)
    ordering = ('school',)
    list_filter = ('added', 'added_by',)
    date_hierarchy = 'added'

    readonly_fields = ('added', 'updated',)

    fieldsets = (
        (None, {
            'fields': ('school', 'texture', 'colors', 'finish', 'vegetables',
                       'energy',),
        }),
        ('Audit', {
            'fields': (('added', 'added_by',), ('updated', 'updated_by',),),
        }),
    )

admin.site.register(FeedbackResponse, FeedbackResponseAdmin)
