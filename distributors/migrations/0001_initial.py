# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Distributor'
        db.create_table('distributors_distributor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('distributors', ['Distributor'])


    def backwards(self, orm):
        
        # Deleting model 'Distributor'
        db.delete_table('distributors_distributor')


    models = {
        'distributors.distributor': {
            'Meta': {'object_name': 'Distributor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['distributors']
