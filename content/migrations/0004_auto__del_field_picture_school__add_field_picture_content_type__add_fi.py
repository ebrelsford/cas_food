# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Picture.school'
        db.delete_column('content_picture', 'school_id')

        # Adding field 'Picture.content_type'
        db.add_column('content_picture', 'content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=14, to=orm['contenttypes.ContentType']), keep_default=False)

        # Adding field 'Picture.object_id'
        db.add_column('content_picture', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=1), keep_default=False)

        # Deleting field 'Video.school'
        db.delete_column('content_video', 'school_id')

        # Adding field 'Video.content_type'
        db.add_column('content_video', 'content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=14, to=orm['contenttypes.ContentType']), keep_default=False)

        # Adding field 'Video.object_id'
        db.add_column('content_video', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=1), keep_default=False)

        # Deleting field 'Note.school'
        db.delete_column('content_note', 'school_id')

        # Adding field 'Note.content_type'
        db.add_column('content_note', 'content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=14, to=orm['contenttypes.ContentType']), keep_default=False)

        # Adding field 'Note.object_id'
        db.add_column('content_note', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Picture.school'
        db.add_column('content_picture', 'school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.School'], null=True, blank=True), keep_default=False)

        # Deleting field 'Picture.content_type'
        db.delete_column('content_picture', 'content_type_id')

        # Deleting field 'Picture.object_id'
        db.delete_column('content_picture', 'object_id')

        # Adding field 'Video.school'
        db.add_column('content_video', 'school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.School'], null=True, blank=True), keep_default=False)

        # Deleting field 'Video.content_type'
        db.delete_column('content_video', 'content_type_id')

        # Deleting field 'Video.object_id'
        db.delete_column('content_video', 'object_id')

        # Adding field 'Note.school'
        db.add_column('content_note', 'school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.School'], null=True, blank=True), keep_default=False)

        # Deleting field 'Note.content_type'
        db.delete_column('content_note', 'content_type_id')

        # Deleting field 'Note.object_id'
        db.delete_column('content_note', 'object_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'content.note': {
            'Meta': {'object_name': 'Note'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'content.picture': {
            'Meta': {'object_name': 'Picture'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'content.video': {
            'Meta': {'object_name': 'Video'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['content']
