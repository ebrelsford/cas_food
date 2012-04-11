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

class Video(BaseContent):
    url = models.TextField()
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

class Picture(BaseContent):
    picture = ImageField(upload_to='pictures')
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

class Note(BaseContent):
    text = models.TextField()
