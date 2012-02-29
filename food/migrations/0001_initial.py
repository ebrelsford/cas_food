# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Dish'
        db.create_table('food_dish', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('food', ['Dish'])

        # Adding model 'Menu'
        db.create_table('food_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('food', ['Menu'])


    def backwards(self, orm):
        
        # Deleting model 'Dish'
        db.delete_table('food_dish')

        # Deleting model 'Menu'
        db.delete_table('food_menu')


    models = {
        'food.dish': {
            'Meta': {'object_name': 'Dish'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'food.menu': {
            'Meta': {'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['food']
