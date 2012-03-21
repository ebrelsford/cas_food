from django.db import models

from distributors.models import Distributor

class Ingredient(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=128)
    distributors = models.ManyToManyField(Distributor, blank=True, null=True, help_text='The distributors who schools get this dish from')
    ingredients = models.ManyToManyField(Ingredient, blank=True, null=True, help_text='The ingredients in this dish')

    # pictures TODO use contenttypes and use those in content.models
    # notes TODO use contenttypes and use those in content.models
    # aliases, other names the school uses for this dish

    class Meta:
        verbose_name_plural = 'dishes'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('food.views.details', (), { 'id': self.id })

class Nutrient(models.Model):
    name = models.CharField(max_length=128)
    daily_recommended_amount = models.IntegerField(blank=True, null=True, help_text='The daily recommended amount of this nutrient, in milligrams') # only in milligrams

    def __unicode__(self):
        return self.name

class NutritionFact(models.Model):
    # TODO auditing
    dish = models.ForeignKey(Dish, help_text='The dish this fact belongs to')
    nutrient = models.ForeignKey(Nutrient, help_text='The nutrient for this fact')
    amount = models.IntegerField(blank=True, null=True, help_text='The amount of this nutrient (in milligrams or calories) in one serving of this dish') # only in milligrams or calories, depending on nutrient
    percent_daily_value = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text='The percent daily value of this nutrient in one serving of this dish')

    def __unicode__(self):
        return self.dish.name + ': ' + self.nutrient.name

class Meal(models.Model):
    # TODO auditing
    SCHOOL_TYPE_CHOICES = (
        ('primary', 'primary'),
        ('secondary', 'secondary'),
    )

    date = models.DateField(help_text='The date this meal is served')
    dishes = models.ManyToManyField(Dish, help_text='The dishes in this meal')
    school_type = models.CharField(max_length=32, choices=SCHOOL_TYPE_CHOICES)

    def __unicode__(self):
        return str(self.date)

    @models.permalink
    def get_absolute_url(self):
        return ('food.views.menu_day', (), { 
            'school_type': self.school_type,
            'year': self.date.year,
            'month': self.date.month,
            'day': self.date.day,
        })
