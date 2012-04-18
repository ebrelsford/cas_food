from django.contrib.flatpages.models import FlatPage
from django.forms import CharField, ModelForm

from ckeditor.widgets import CKEditorWidget

class FlatPageForm(ModelForm):
    content = CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        exclude = ('url', 'enable_comments', 'template_name',
                   'registration_required', 'sites',)
