from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage

from ckeditor.widgets import CKEditorWidget

from pages.models import SectionedFlatPage

class FlatPageAdminForm(forms.ModelForm):
    """Override standard admin form for flatpages"""
    content = forms.CharField(widget=CKEditorWidget(config_name='admin'))

    class Meta:
        model = FlatPage

class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageAdminForm

class SectionedFlatPageAdmin(FlatPageAdmin):
    class Meta:
        model = SectionedFlatPage

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(SectionedFlatPage, SectionedFlatPageAdmin)
