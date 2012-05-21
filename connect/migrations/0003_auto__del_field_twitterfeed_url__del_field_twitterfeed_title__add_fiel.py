# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'TwitterFeed.url'
        db.delete_column('connect_twitterfeed', 'url')

        # Deleting field 'TwitterFeed.title'
        db.delete_column('connect_twitterfeed', 'title')

        # Adding field 'TwitterFeed.handle'
        db.add_column('connect_twitterfeed', 'handle', self.gf('django.db.models.fields.CharField')(default='', max_length=56), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'TwitterFeed.url'
        raise RuntimeError("Cannot reverse this migration. 'TwitterFeed.url' and its values cannot be restored.")

        # Adding field 'TwitterFeed.title'
        db.add_column('connect_twitterfeed', 'title', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True), keep_default=False)

        # Deleting field 'TwitterFeed.handle'
        db.delete_column('connect_twitterfeed', 'handle')


    models = {
        'connect.twitterfeed': {
            'Meta': {'object_name': 'TwitterFeed'},
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'connect.video': {
            'Meta': {'object_name': 'Video'},
            'embed_code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['connect']
