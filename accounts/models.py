from django.db import models
from django.contrib.auth.models import User

from schools.models import School

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    schools_following = models.ManyToManyField(School, related_name='followers',
                                               help_text='The schools this user is following')

    def __unicode__(self):
        return self.user.username

    class Meta:
        permissions = (
            ('can_follow_schools', 'Can follow schools'),
        )
