from django import forms

from selectable.forms.widgets import AutoCompleteWidget

from schools.lookups import SchoolLookup

class SchoolSearchForm(forms.Form):
    school = forms.CharField(
        label='School name or an address',
        widget=AutoCompleteWidget(SchoolLookup, allow_new=True),
        required=True
    )
