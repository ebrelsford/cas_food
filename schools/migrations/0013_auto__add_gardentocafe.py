# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GardenToCafe'
        db.create_table('schools_gardentocafe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.School'])),
            ('garden_coordinators', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('schools', ['GardenToCafe'])


    def backwards(self, orm):
        
        # Deleting model 'GardenToCafe'
        db.delete_table('schools_gardentocafe')


    models = {
        'schools.gardentocafe': {
            'Meta': {'object_name': 'GardenToCafe'},
            'garden_coordinators': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schools.School']"})
        },
        'schools.school': {
            'Meta': {'object_name': 'School'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'admin_district': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'geo_district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'has_content': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'participates_in_garden_to_cafe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participates_in_wellness_in_the_schools': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schools']
