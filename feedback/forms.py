from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelForm, ModelChoiceField, CharField, IntegerField, RadioSelect

from schools.models import School
from models import FeedbackResponse

class FeedbackResponseForm(ModelForm):
    texture = CharField(
        widget=RadioSelect(
            choices=(
                ('mushy', 'mushy'),
                ('crunchy', 'crunchy'),
                ('soggy', 'soggy'),
            ),
        )
    )
    colors = CharField(
        widget=RadioSelect(
            choices=(
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4 or more'),
            )
        )
    )
    vegetables = CharField(
        widget=RadioSelect(
            choices=(
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4 or more'),
            )
        )
    )
    energy = CharField(
        widget=RadioSelect(
            choices=(
                ('energetic', 'energetic'),
                ('sleepy', 'sleepy'),
            )
        )
    )
    finish = IntegerField(
        initial=0,
        widget=HiddenInput()
    )
    school = ModelChoiceField(
        queryset=School.objects.all(),
        widget=HiddenInput()
    )
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = FeedbackResponse
