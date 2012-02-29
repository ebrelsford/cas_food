from django import forms

class SchoolSearchForm(forms.Form):
    search_text = forms.CharField(max_length=512)
