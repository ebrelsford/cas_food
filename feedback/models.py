from django.db import models

from audit.models import AuditedModel
from schools.models import School

class FeedbackResponse(AuditedModel):
    """A response to the feedback quiz"""
    
    school = models.ForeignKey(School, help_text='the school the student who created this response goes to')
    
    texture = models.CharField(max_length=16, choices=(
        ('mushy', 'mushy'),
        ('crunchy', 'crunchy'),
        ('soggy', 'soggy'),
    ), help_text='What was the texture of the food today?')

    colors = models.CharField(
        max_length=32, 
        help_text='How many colors were on your tray today?'
    )

    finish = models.PositiveIntegerField(
        default=0,
        help_text='Did you finish your meal?'
    )

    vegetables = models.PositiveIntegerField(
        help_text='How many vegetables were on your tray today?'
    )

    energy = models.CharField(max_length=32, choices=(
        ('energetic', 'energetic'),
        ('sleepy', 'sleepy'),
    ), help_text='Were you sleepy or energetic after your meal?')

    new_food = models.BooleanField(
        default=False,
        help_text='did you try a new type of food today during lunch?'
    )

    def __unicode__(self):
        return self.school.name + ', ' + self.added_by.username
