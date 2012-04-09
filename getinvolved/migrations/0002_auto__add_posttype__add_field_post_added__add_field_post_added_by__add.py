# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PostType'
        db.create_table('getinvolved_posttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('getinvolved', ['PostType'])

        # Adding field 'Post.added'
        db.add_column('getinvolved_post', 'added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 9, 11, 39, 51, 847951), blank=True), keep_default=False)

        # Adding field 'Post.added_by'
        db.add_column('getinvolved_post', 'added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='getinvolved_post_added', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Post.updated'
        db.add_column('getinvolved_post', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 9, 11, 40, 2, 936528), blank=True), keep_default=False)

        # Adding field 'Post.updated_by'
        db.add_column('getinvolved_post', 'updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='getinvolved_post_updated', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Post.title'
        db.add_column('getinvolved_post', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)

        # Adding field 'Post.type'
        db.add_column('getinvolved_post', 'type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['getinvolved.PostType'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'PostType'
        db.delete_table('getinvolved_posttype')

        # Deleting field 'Post.added'
        db.delete_column('getinvolved_post', 'added')

        # Deleting field 'Post.added_by'
        db.delete_column('getinvolved_post', 'added_by_id')

        # Deleting field 'Post.updated'
        db.delete_column('getinvolved_post', 'updated')

        # Deleting field 'Post.updated_by'
        db.delete_column('getinvolved_post', 'updated_by_id')

        # Deleting field 'Post.title'
        db.delete_column('getinvolved_post', 'title')

        # Deleting field 'Post.type'
        db.delete_column('getinvolved_post', 'type_id')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 9, 11, 40, 7, 270162)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 9, 11, 40, 7, 269982)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'getinvolved.post': {
            'Meta': {'object_name': 'Post'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'getinvolved_post_added'", 'null': 'True', 'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['getinvolved.PostType']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'getinvolved_post_updated'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'getinvolved.posttype': {
            'Meta': {'object_name': 'PostType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['getinvolved']
