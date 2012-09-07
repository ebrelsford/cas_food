from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

class Alias(models.Model):
    text = models.CharField(max_length=256)

    aliased_type = models.ForeignKey(ContentType)
    aliased_object_id = models.PositiveIntegerField()
    aliased_object = generic.GenericForeignKey('aliased_type', 'aliased_object_id')

    class Meta:
        verbose_name_plural = 'aliases'

    def __unicode__(self):
        return self.text

class AliasManager(models.Manager):

    def __init__(self, aliased_field_name=None):
        super(AliasManager, self).__init__()
        self.aliased_field_name = aliased_field_name

    def with_alias(self, alias):
        """
        Get all objects with the given alias or that match in the aliased 
        field.
        """
        aliased_pks = Alias.objects.filter(
            text=alias,
            aliased_type=ContentType.objects.get_for_model(self.model)
        ).values_list('aliased_object_id', flat=True)

        return super(AliasManager, self).get_query_set().filter(
            Q(pk__in=aliased_pks) |
            Q(**{
                self.aliased_field_name: alias
            })
        )
