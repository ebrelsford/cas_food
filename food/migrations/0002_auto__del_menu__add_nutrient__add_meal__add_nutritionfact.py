# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Menu'
        db.delete_table('food_menu')

        # Adding model 'Nutrient'
        db.create_table('food_nutrient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('daily_recommended_amount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('food', ['Nutrient'])

        # Adding model 'Meal'
        db.create_table('food_meal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('food', ['Meal'])

        # Adding M2M table for field dishes on 'Meal'
        db.create_table('food_meal_dishes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meal', models.ForeignKey(orm['food.meal'], null=False)),
            ('dish', models.ForeignKey(orm['food.dish'], null=False))
        ))
        db.create_unique('food_meal_dishes', ['meal_id', 'dish_id'])

        # Adding model 'NutritionFact'
        db.create_table('food_nutritionfact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['food.Dish'])),
            ('nutrient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['food.Nutrient'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('percent_daily_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1, blank=True)),
        ))
        db.send_create_signal('food', ['NutritionFact'])

        # Adding M2M table for field distributors on 'Dish'
        db.create_table('food_dish_distributors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dish', models.ForeignKey(orm['food.dish'], null=False)),
            ('distributor', models.ForeignKey(orm['distributors.distributor'], null=False))
        ))
        db.create_unique('food_dish_distributors', ['dish_id', 'distributor_id'])


    def backwards(self, orm):
        
        # Adding model 'Menu'
        db.create_table('food_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('food', ['Menu'])

        # Deleting model 'Nutrient'
        db.delete_table('food_nutrient')

        # Deleting model 'Meal'
        db.delete_table('food_meal')

        # Removing M2M table for field dishes on 'Meal'
        db.delete_table('food_meal_dishes')

        # Deleting model 'NutritionFact'
        db.delete_table('food_nutritionfact')

        # Removing M2M table for field distributors on 'Dish'
        db.delete_table('food_dish_distributors')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
