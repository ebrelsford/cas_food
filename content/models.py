from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from sorl.thumbnail import ImageField

class BaseContent(models.Model):
    """a piece of content that can be attached to anything"""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    class Meta:
        abstract = True

class Picture(BaseContent):
    picture = ImageField(upload_to='pictures')
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

class Note(BaseContent):
    text = models.TextField()

class Section(BaseContent):
    """A section of a page"""
    title = models.CharField(max_length=256)
    text = models.TextField()

    weight = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return 'Section: ' + self.title   

    @models.permalink
    def get_absolute_url(self):
        return ('content_section_detail', (self.id,))
