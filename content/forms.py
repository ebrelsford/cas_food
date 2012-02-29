from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelForm, ModelChoiceField

from schools.models import School
from models import Note, Picture, Video
 
class ContentForm(ModelForm):
    school = ModelChoiceField(label='school', queryset=School.objects.all(), widget=HiddenInput())
    added_by = ModelChoiceField(label='added_by', queryset=User.objects.all(), widget=HiddenInput())

    class Meta:
        exclude = 'added'

class NoteForm(ContentForm):
    class Meta:
        model = Note

class PictureForm(ContentForm):
    class Meta:
        model = Picture

class VideoForm(ContentForm):
    class Meta:
        model = Video
