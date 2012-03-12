from django.db import models

class Distributor(models.Model):
    name = models.CharField(max_length=256)
    # address
    # POINT
    # website
