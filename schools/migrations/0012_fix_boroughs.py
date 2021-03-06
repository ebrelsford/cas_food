# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
    boroughs = {
        'K': 'Brooklyn',
        'M': 'Manhattan',
        'Q': 'Queens',
        'R': 'Staten Island',
        'X': 'Bronx',
    }

    def forwards(self, orm):
        "Update boroughs. Give them names!"
        for symbol,name in self.boroughs.items():
            orm.School.objects.filter(borough=symbol).update(borough=name)

    def backwards(self, orm):
        "Un-update boroughs. Take away their names!"
        for symbol,name in self.boroughs.items():
            orm.School.objects.filter(borough=name).update(borough=symbol)


    models = {
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
