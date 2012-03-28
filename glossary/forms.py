from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput, ModelChoiceField

from glossary.models import Entry

class EntryForm(ModelForm):
    """Generic Entry form without auditing"""
    class Meta:
        model = Entry
        exclude = ('slug',)

class AddEntryForm(EntryForm):
    """Add Entry form with auditing"""
    added_by = ModelChoiceField(label='added_by', queryset=User.objects.all(), widget=HiddenInput())

    class Meta(EntryForm.Meta):
        exclude = EntryForm.Meta.exclude + ('updated_by',)

class ChangeEntryForm(EntryForm):
    """Change Entry form with auditing"""
    updated_by = ModelChoiceField(label='updated_by', queryset=User.objects.all(), widget=HiddenInput())

    class Meta(EntryForm.Meta):
        exclude = EntryForm.Meta.exclude + ('added_by',)
