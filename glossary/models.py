from django.db import models

from audit.models import AuditedModel
from cas_food.utils import slugify

class Entry(AuditedModel):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    text = models.TextField()

    class Meta:
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('glossary_entry_detail', (self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(Entry, self)
        super(Entry, self).save(*args, **kwargs)
