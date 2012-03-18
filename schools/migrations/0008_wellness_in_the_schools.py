# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    participating_school_names = (
        'P.S. 011 WILLIAM T. HARRIS',
        'P.S. 003 CHARRETTE SCHOOL',
        'P.S. 098 SHORAC KAPPOCK',
        'P.S. X811',
        'P.S. 041 GREENWICH VILLAGE',
        'P.S. 333 MANHATTAN SCHOOL FOR CHILDREN',
        #'Hunter College Elementary School', #TODO could not find
        'P.S. 166 THE RICHARD RODGERS SCHOOL OF THE ARTS AN',
        'P.S. 084 LILLIAN WEBER',
        'P.S. 199 JESSIE ISADOR STRAUS',
        'M.S. M245 THE COMPUTER SCHOOL',
        'P.S./I.S. 278',
        'P.S. 112 BRONXWOOD',
        'MUSCOTA',
    )

    def forwards(self, orm):
        "Set flag for schools that participate in Wellness in the Schools"
        orm.School.objects.filter(name__in=self.participating_school_names).update(participates_in_wellness_in_the_schools=True)

    def backwards(self, orm):
        "Unset flag for schools that participate in Wellness in the Schools"
        orm.School.objects.filter(name__in=self.participating_school_names).update(participates_in_wellness_in_the_schools=False)


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
            'participates_in_wellness_in_the_schools': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schools']
