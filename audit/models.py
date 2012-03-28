from django.contrib.auth.models import User
from django.db import models

class AuditedModel(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_added', blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_updated', blank=True, null=True)

    class Meta:
        abstract = True
