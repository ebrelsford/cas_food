import re

from django.contrib.contenttypes import generic
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from content.models import Note
from notify.notifiers import NewNoteNotifier

class School(models.Model):
    slug = models.SlugField(max_length=260)
    name = models.CharField(max_length=256)
    ats_code = models.CharField(max_length=16, null=True, blank=True, help_text='an NYC-wide unique school ID')

    address = models.CharField(max_length=256, null=True, blank=True)
    borough = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)

    type = models.CharField(max_length=128, null=True, blank=True)
    grades = models.CharField(max_length=128, null=True, blank=True)

    admin_district = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    geo_district = models.IntegerField(null=True, blank=True)

    has_content = models.BooleanField(default=False)
    participates_in_wellness_in_the_schools = models.BooleanField(default=False)
    participates_in_garden_to_cafe = models.BooleanField(default=False)

    point = models.PointField()
    objects = models.GeoManager()

    notes = generic.GenericRelation(Note)

    def __unicode__(self):
        return '%s %s' % (self.name, self.city,)

    def _get_school_food_code(self):
        """Get the school food code, which is the ats_code minus the county character"""
        school_food_code, i = re.subn('\D+', '', self.ats_code)
        return school_food_code
    school_food_code = property(_get_school_food_code)

class Contact(models.Model):
    """A person at a school who might be worth contacting"""
    school = models.ForeignKey(School)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=64, null=True, blank=True, choices=(
        ('principal', 'principal'),
    ))
    phone = models.CharField(max_length=32, null=True, blank=True)
    
    def __unicode__(self):
        return self.name + ': ' + self.school.name

class GardenToCafe(models.Model):
    school = models.ForeignKey(School)
    garden_coordinators = models.CharField(max_length=256)
    organization = models.CharField(max_length=256)

    def __unicode__(self):
        return str(self.school)

@receiver(post_save, sender=Note)
def note_create_notify_followers(sender, instance=None, created=False, **kwargs):
    """notify followers when a note is added to a school they are following"""
    if created and instance.content_type.model_class() == School:
        NewNoteNotifier(instance).send()
