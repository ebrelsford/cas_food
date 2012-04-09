from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from models import Post, PostType

class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(config_name='admin'))

    class Meta:
        model = Post

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'type', 'added', 'added_by',)
    list_filter = ('type', 'added', 'added_by',)
    search_fields = ('text', 'title',)
    date_hierarchy = 'added'

    readonly_fields = ('added', 'updated',)

    fieldsets = (
        (None, {
            'fields': ('title', 'text',),
        }),
        ('Audit', {
            'fields': (('added', 'added_by',), ('updated', 'updated_by',),),
        }),
    )

class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(PostType, PostTypeAdmin)
