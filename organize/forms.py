from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.forms import HiddenInput, IntegerField, ModelForm, ModelChoiceField

from models import Organizer
 
class OrganizerForm(ModelForm):
    content_type = ModelChoiceField(
        label='content_type',
        queryset=ContentType.objects.all(),
        widget=HiddenInput()
    )
    object_id = IntegerField(
        label='object_id',
        min_value=1, 
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        """Use a pass object kwarg to get the content_type and object_id"""

        # find object
        if 'object' not in kwargs:
            raise Exception('OrganizerForm requires keyword argument "object"')
        object = kwargs.pop('object')

        # add to initial
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        kwargs['initial'].update({
            'object_id': object.id,
            'content_type': ContentType.objects.get_for_model(object),
        })
        super(OrganizerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organizer
        widgets = {
            'object_id': HiddenInput(),
        }

class AddOrganizerForm(OrganizerForm):
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(), 
        widget=HiddenInput()
    )

    class Meta(OrganizerForm.Meta):
        exclude = ('added', 'updated', 'updated_by')

class EditOrganizerForm(OrganizerForm):
    updated_by = ModelChoiceField(
        label='updated_by',
        queryset=User.objects.all(), 
        widget=HiddenInput()
    )

    class Meta(OrganizerForm.Meta):
        exclude = ('added', 'added_by', 'updated')
