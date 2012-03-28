from django.forms import ModelForm

from glossary.models import Entry

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        exclude = ('slug',)
