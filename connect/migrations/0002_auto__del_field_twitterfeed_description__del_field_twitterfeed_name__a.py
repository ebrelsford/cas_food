# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'TwitterFeed.description'
        db.delete_column('connect_twitterfeed', 'description')

        # Deleting field 'TwitterFeed.name'
        db.delete_column('connect_twitterfeed', 'name')

        # Adding field 'TwitterFeed.title'
        db.add_column('connect_twitterfeed', 'title', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True), keep_default=False)

        # Adding field 'TwitterFeed.text'
        db.add_column('connect_twitterfeed', 'text', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Video.description'
        db.delete_column('connect_video', 'description')

        # Deleting field 'Video.name'
        db.delete_column('connect_video', 'name')

        # Adding field 'Video.title'
        db.add_column('connect_video', 'title', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True), keep_default=False)

        # Adding field 'Video.text'
        db.add_column('connect_video', 'text', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'TwitterFeed.description'
        db.add_column('connect_twitterfeed', 'description', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'TwitterFeed.name'
        db.add_column('connect_twitterfeed', 'name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True), keep_default=False)

        # Deleting field 'TwitterFeed.title'
        db.delete_column('connect_twitterfeed', 'title')

        # Deleting field 'TwitterFeed.text'
        db.delete_column('connect_twitterfeed', 'text')

        # Adding field 'Video.description'
        db.add_column('connect_video', 'description', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Video.name'
        db.add_column('connect_video', 'name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True), keep_default=False)

        # Deleting field 'Video.title'
        db.delete_column('connect_video', 'title')

        # Deleting field 'Video.text'
        db.delete_column('connect_video', 'text')


    models = {
        'connect.twitterfeed': {
            'Meta': {'object_name': 'TwitterFeed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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
