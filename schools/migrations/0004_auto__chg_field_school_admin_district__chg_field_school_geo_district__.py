# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'School.admin_district'
        db.alter_column('schools_school', 'admin_district', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3))

        # Changing field 'School.geo_district'
        db.alter_column('schools_school', 'geo_district', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'School.zip_code'
        db.alter_column('schools_school', 'zip_code', self.gf('django.db.models.fields.IntegerField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'School.admin_district'
        db.alter_column('schools_school', 'admin_district', self.gf('django.db.models.fields.CharField')(max_length=8, null=True))

        # Changing field 'School.geo_district'
        db.alter_column('schools_school', 'geo_district', self.gf('django.db.models.fields.CharField')(max_length=8, null=True))

        # Changing field 'School.zip_code'
        db.alter_column('schools_school', 'zip_code', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))


    models = {
        'schools.school': {
            'Meta': {'object_name': 'School'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'admin_district': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'ats_code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'geo_district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schools']
