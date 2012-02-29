# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'School.centroid'
        db.delete_column('schools_school', 'centroid')

        # Adding field 'School.borough'
        db.add_column('schools_school', 'borough', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True), keep_default=False)

        # Adding field 'School.zip_code'
        db.add_column('schools_school', 'zip_code', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True), keep_default=False)

        # Adding field 'School.type'
        db.add_column('schools_school', 'type', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True), keep_default=False)

        # Adding field 'School.grades'
        db.add_column('schools_school', 'grades', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True), keep_default=False)

        # Adding field 'School.ats_code'
        db.add_column('schools_school', 'ats_code', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True), keep_default=False)

        # Adding field 'School.geo_district'
        db.add_column('schools_school', 'geo_district', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True), keep_default=False)

        # Adding field 'School.admin_district'
        db.add_column('schools_school', 'admin_district', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True), keep_default=False)

        # Adding field 'School.point'
        db.add_column('schools_school', 'point', self.gf('django.contrib.gis.db.models.fields.PointField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'School.centroid'
        db.add_column('schools_school', 'centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True), keep_default=False)

        # Deleting field 'School.borough'
        db.delete_column('schools_school', 'borough')

        # Deleting field 'School.zip_code'
        db.delete_column('schools_school', 'zip_code')

        # Deleting field 'School.type'
        db.delete_column('schools_school', 'type')

        # Deleting field 'School.grades'
        db.delete_column('schools_school', 'grades')

        # Deleting field 'School.ats_code'
        db.delete_column('schools_school', 'ats_code')

        # Deleting field 'School.geo_district'
        db.delete_column('schools_school', 'geo_district')

        # Deleting field 'School.admin_district'
        db.delete_column('schools_school', 'admin_district')

        # Deleting field 'School.point'
        db.delete_column('schools_school', 'point')


    models = {
        'schools.school': {
            'Meta': {'object_name': 'School'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'admin_district': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'ats_code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'geo_district': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'grades': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schools']
