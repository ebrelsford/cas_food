from django.contrib.auth.models import User
from django.forms import DateTimeField, DateInput, ModelForm, HiddenInput, ModelChoiceField, ImageField

from content.models import Picture
from schools.models import School
from models import Tray

class TrayForm(ModelForm):
    date = DateTimeField(label='Date',
                         widget=DateInput(attrs={'class': 'date no-future'}))
    added_by = ModelChoiceField(label='added_by', queryset=User.objects.all(),
                                widget=HiddenInput())
    school = ModelChoiceField(label='school', queryset=School.objects.all(),
                              widget=HiddenInput())
    picture = ImageField()

    class Meta:
        exclude = ('updated_by',)
        model = Tray

    def save(self, force_insert=False, force_update=False, commit=True):
        picture = self.cleaned_data.pop('picture')
        tray = super(TrayForm, self).save()
        p = Picture(
            added_by=self.cleaned_data['added_by'],
            content_object=tray,
            picture=picture
        )
        p.save()
        return tray
