from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from content.models import Section

class SectionAdminForm(forms.ModelForm):
    """Override standard admin form for flatpages"""
    text = forms.CharField(widget=CKEditorWidget(config_name='admin'))

    class Meta:
        model = Section

class SectionAdmin(admin.ModelAdmin):
    form = SectionAdminForm
    list_display = ('title', 'content_type',)

admin.site.register(Section, SectionAdmin)
