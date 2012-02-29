from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from sorl.thumbnail import ImageField

from schools.models import School

class BaseContent(models.Model):
    school = models.ForeignKey(School, null=True, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    class Meta:
        abstract = True

class Video(BaseContent):
    url = models.TextField()
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

class Picture(BaseContent):
    picture = ImageField(upload_to='pictures')
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

class Note(BaseContent):
    title = models.CharField(max_length=256)
    text = models.TextField()

@receiver(post_save, sender=Video)
@receiver(post_save, sender=Picture)
@receiver(post_save, sender=Note)
def mark_school_has_content(sender, **kwargs):
    school = kwargs['instance'].school
    if not school.has_content:
        school.has_content = True
        school.save()
