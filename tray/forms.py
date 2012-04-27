from django.contrib.auth.models import User
from django.forms import DateTimeField, DateInput, ModelForm, HiddenInput, ModelChoiceField

from schools.models import School
from models import Tray

class TrayForm(ModelForm):
    date = DateTimeField(label='Date',
                         widget=DateInput(attrs={'class': 'date no-future'}))
    added_by = ModelChoiceField(label='added_by', queryset=User.objects.all(),
                                widget=HiddenInput())
    school = ModelChoiceField(label='school', queryset=School.objects.all(),
                              widget=HiddenInput())

    class Meta:
        exclude = ('updated_by',)
        model = Tray
