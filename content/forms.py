from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.forms import HiddenInput, IntegerField, ModelForm, ModelChoiceField

from models import Note, Picture, Video
 
class ContentForm(ModelForm):
    content_type = ModelChoiceField(label='content_type', queryset=ContentType.objects.all(), widget=HiddenInput())
    object_id = IntegerField(label='object_id', min_value=1, widget=HiddenInput())
    added_by = ModelChoiceField(label='added_by', queryset=User.objects.all(), widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        """Use a pass object kwarg to get the content_type and object_id"""

        # find object
        if 'object' not in kwargs:
            raise Exception('ContentForm requires keyword argument "object"')
        object = kwargs.pop('object')

        # add to initial
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        kwargs['initial'].update({
            'object_id': object.id,
            'content_type': ContentType.objects.get_for_model(object),
        })
        super(ContentForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = 'added'
        widgets = {
            'object_id': HiddenInput(),
        }

class NoteForm(ContentForm):
    class Meta:
        model = Note

class PictureForm(ContentForm):
    class Meta:
        model = Picture

class VideoForm(ContentForm):
    class Meta:
        model = Video
