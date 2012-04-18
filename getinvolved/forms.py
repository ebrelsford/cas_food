from django.contrib.auth.models import User
from django.forms import CharField, HiddenInput, ModelForm, ModelChoiceField

from ckeditor.widgets import CKEditorWidget

from models import Post

class PostForm(ModelForm):
    text = CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        exclude = ('added', 'updated',)

class PostCreateForm(PostForm):
    added_by = ModelChoiceField(label='added_by', queryset=User.objects.all(),
                                widget=HiddenInput())

    class Meta(PostForm.Meta):
        exclude = PostForm.Meta.exclude + ('updated_by',)

class PostUpdateForm(PostForm):
    updated_by = ModelChoiceField(label='updated_by',
                                  queryset=User.objects.all(),
                                  widget=HiddenInput())

    class Meta(PostForm.Meta):
        exclude = PostForm.Meta.exclude + ('added_by',)
