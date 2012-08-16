from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from content.models import Note, Picture, Section, Video

class SectionAdminForm(forms.ModelForm):
    """Override standard admin form for flatpages"""
    text = forms.CharField(widget=CKEditorWidget(config_name='admin'))

    class Meta:
        model = Section

class NoteAdmin(admin.ModelAdmin):
    list_display = ('added_by', 'added',)

class PictureAdmin(admin.ModelAdmin):
    list_display = ('title', 'added_by', 'added',)

class SectionAdmin(admin.ModelAdmin):
    form = SectionAdminForm
    list_display = ('title', 'content_type',)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'added_by', 'added',)

admin.site.register(Note, NoteAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Video, VideoAdmin)
