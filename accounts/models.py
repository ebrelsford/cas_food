import logging

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import models
from django.dispatch import receiver

from registration.signals import user_registered

from schools.models import School

logger = logging.getLogger(__name__)

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

@receiver(user_registered)
def add_user_to_default_group(sender, user=None, request=None, **kwargs):
    """
    When a user is registered, add it to the default group, as specified with 
    settings.DEFAULT_GROUP.
    """
    try:
        group = Group.objects.get(name=settings.DEFAULT_GROUP)
        user.groups.add(group)
        user.save()
    except:
        logger.warn('Failed to add user to settings.DEFAULT_GROUP. Is there '
                    'such a group?')
