from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from audit.models import AuditedModel

class Organizer(AuditedModel):
    """
    Someone or something organizing something else.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField()
    url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        # TODO implement
        return ('view_or_url_name' )
