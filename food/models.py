from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=128)

    # nutritional facts (name, measurement--'0g', '10%')

    # pictures

    # notes

    # where it's generally sourced from

class Menu(models.Model):
    pass

    # date

    # Dishes
