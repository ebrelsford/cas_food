# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Meal.school_type'
        db.add_column('food_meal', 'school_type', self.gf('django.db.models.fields.CharField')(default='primary', max_length=32), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Meal.school_type'
        db.delete_column('food_meal', 'school_type')


    models = {
        'distributors.distributor': {
            'Meta': {'object_name': 'Distributor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'food.dish': {
            'Meta': {'object_name': 'Dish'},
            'distributors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['distributors.Distributor']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'food.meal': {
            'Meta': {'object_name': 'Meal'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'dishes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['food.Dish']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school_type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'food.nutrient': {
            'Meta': {'object_name': 'Nutrient'},
            'daily_recommended_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'food.nutritionfact': {
            'Meta': {'object_name': 'NutritionFact'},
            'amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['food.Dish']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nutrient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['food.Nutrient']"}),
            'percent_daily_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['food']
