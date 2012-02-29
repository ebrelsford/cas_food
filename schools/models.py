from django.contrib.gis.db import models

class School(models.Model):
    name = models.CharField(max_length=256)

    address = models.CharField(max_length=256, null=True, blank=True)
    borough = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)

    type = models.CharField(max_length=128, null=True, blank=True)
    grades = models.CharField(max_length=128, null=True, blank=True)

    admin_district = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    ats_code = models.CharField(max_length=32, null=True, blank=True)
    geo_district = models.IntegerField(null=True, blank=True)

    has_content = models.BooleanField(default=False)

    point = models.PointField()
    objects = models.GeoManager()
