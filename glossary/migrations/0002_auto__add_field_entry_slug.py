# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Entry.slug'
        db.add_column('glossary_entry', 'slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=256, db_index=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Entry.slug'
        db.delete_column('glossary_entry', 'slug')


    models = {
        'glossary.entry': {
            'Meta': {'object_name': 'Entry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['glossary']
