# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'groupapp_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('picture', self.gf('groupapp.croppable.fields.CroppableImageField')(invalidate_on_save='from south', crop_widget='from south', max_length=100, blank=True)),
        ))
        db.send_create_signal(u'groupapp', ['UserProfile'])

        # Adding model 'Group'
        db.create_table(u'groupapp_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.UserProfile'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('privacy', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('joining', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'groupapp', ['Group'])

        # Adding model 'UserGroup'
        db.create_table(u'groupapp_usergroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.UserProfile'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.Group'])),
            ('allow_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_administrator', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'groupapp', ['UserGroup'])

        # Adding model 'Thread'
        db.create_table(u'groupapp_thread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.UserProfile'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.Group'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groupapp', ['Thread'])

        # Adding model 'Post'
        db.create_table(u'groupapp_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.UserProfile'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.Thread'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'groupapp', ['Post'])

        # Adding model 'Like'
        db.create_table(u'groupapp_like', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.UserProfile'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'groupapp', ['Like'])

        # Adding model 'Follow'
        db.create_table(u'groupapp_follow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupapp.UserProfile'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'groupapp', ['Follow'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'groupapp_userprofile')

        # Deleting model 'Group'
        db.delete_table(u'groupapp_group')

        # Deleting model 'UserGroup'
        db.delete_table(u'groupapp_usergroup')

        # Deleting model 'Thread'
        db.delete_table(u'groupapp_thread')

        # Deleting model 'Post'
        db.delete_table(u'groupapp_post')

        # Deleting model 'Like'
        db.delete_table(u'groupapp_like')

        # Deleting model 'Follow'
        db.delete_table(u'groupapp_follow')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'groupapp.follow': {
            'Meta': {'object_name': 'Follow'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'groupapp.group': {
            'Meta': {'object_name': 'Group'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joining': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'privacy': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'groupapp.like': {
            'Meta': {'object_name': 'Like'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'groupapp.post': {
            'Meta': {'object_name': 'Post'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.Thread']"})
        },
        u'groupapp.thread': {
            'Meta': {'object_name': 'Thread'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.UserProfile']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'groupapp.usergroup': {
            'Meta': {'object_name': 'UserGroup'},
            'allow_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupapp.UserProfile']"})
        },
        u'groupapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('groupapp.croppable.fields.CroppableImageField', [], {'invalidate_on_save': "'from south'", 'crop_widget': "'from south'", 'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['groupapp']