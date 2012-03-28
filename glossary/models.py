from django.db import models
from django.template.defaultfilters import slugify

from audit.models import AuditedModel

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
        def _make_slug(entry):
            """make a unique slug for this entry"""
            slug = slugify(entry.title)
            same_slug_count = Entry.objects.filter(slug__iregex=slug + '(-\d+)?').count()
            if same_slug_count:
                slug = "%s-%d" % (slug, same_slug_count)
            return slug

        if not self.slug:
            self.slug = _make_slug(self)
        super(Entry, self).save(*args, **kwargs)
