from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from sorl.thumbnail import ImageField

from audit.models import AuditedModel
from content.models import Note
from notify.notifiers import NewTrayNotifier
from schools.models import School

class Tray(AuditedModel):
    """A picture of a lunch tray for rating and discussion."""
    picture = ImageField(upload_to='pictures', help_text='a picture of the tray')
    date = models.DateField(help_text='the date the meal in this tray was served')
    description = models.TextField(null=True, blank=True, help_text='describe the meal on the tray')
    school = models.ForeignKey(School, help_text='the school this tray is from')
    notes = generic.GenericRelation(Note, help_text='comments on this tray')

    def __unicode__(self):
        return self.school.name + str(self.date)

    @models.permalink
    def get_absolute_url(self):
        return ('tray.views.details', (), {
            'school_slug': self.school.slug,
            'tray_id': self.id,
        })

class Rating(AuditedModel):
    tray = models.ForeignKey(Tray, help_text='the tray being rated')
    points = models.PositiveIntegerField(help_text='the points given to the tray')

@receiver(post_save, sender=Tray)
def tray_create_notify_followers(sender, instance=None, created=False, **kwargs):
    """notify followers when a tray is created"""
    if created:
        NewTrayNotifier(instance).send()
