# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing M2M table for field distributors on 'Dish'
        db.delete_table('food_dish_distributors')


    def backwards(self, orm):
        
        # Adding M2M table for field distributors on 'Dish'
        db.create_table('food_dish_distributors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dish', models.ForeignKey(orm['food.dish'], null=False)),
            ('distributor', models.ForeignKey(orm['distributors.distributor'], null=False))
        ))
        db.create_unique('food_dish_distributors', ['dish_id', 'distributor_id'])


    models = {
        'food.dish': {
            'Meta': {'object_name': 'Dish'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['food.Ingredient']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '132', 'db_index': 'True'})
        },
        'food.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'food.meal': {
            'Meta': {'object_name': 'Meal'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'dishes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['food.Dish']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school_type': ('django.db.models.fields.CharField', [], {'default': "'elementary'", 'max_length': '32'})
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
