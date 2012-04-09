from django.db import models

from audit.models import AuditedModel

class PostType(models.Model):
    """A type of post"""
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name    

class Post(AuditedModel):
    """A post about getting involved"""
    title = models.CharField(max_length=128)
    text = models.TextField()
    type = models.ForeignKey(PostType, null=True)
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('getinvolved_post_detail', (), { 'pk': self.id })
