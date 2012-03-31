from django.contrib.contenttypes import generic
from django.contrib.gis.db import models

from content.models import Note

class School(models.Model):
    slug = models.SlugField(max_length=260)
    name = models.CharField(max_length=256)

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

class GardenToCafe(models.Model):
    school = models.ForeignKey(School)
    garden_coordinators = models.CharField(max_length=256)
    organization = models.CharField(max_length=256)

    def __unicode__(self):
        return str(self.school)
