# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RegistrationManager'
        db.create_table(u'accounts_registrationmanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('confirmation_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal(u'accounts', ['RegistrationManager'])


    def backwards(self, orm):
        # Deleting model 'RegistrationManager'
        db.delete_table(u'accounts_registrationmanager')


    models = {
        u'accounts.registrationmanager': {
            'Meta': {'object_name': 'RegistrationManager'},
            'confirmation_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['accounts']