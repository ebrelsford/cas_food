from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    embed_code = models.TextField()
    url = models.URLField()

    def __unicode__(self):
        return self.title

class TwitterFeed(models.Model):
    handle = models.CharField(max_length=56)
    text = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.handle
