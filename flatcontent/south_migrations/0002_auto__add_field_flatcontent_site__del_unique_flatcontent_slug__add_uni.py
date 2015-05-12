# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'FlatContent', fields ['slug']
        db.delete_unique('flatcontent_flatcontent', ['slug'])

        # Adding field 'FlatContent.site'
        db.add_column('flatcontent_flatcontent', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'FlatContent', fields ['slug', 'site']
        db.create_unique('flatcontent_flatcontent', ['slug', 'site_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'FlatContent', fields ['slug', 'site']
        db.delete_unique('flatcontent_flatcontent', ['slug', 'site_id'])

        # Deleting field 'FlatContent.site'
        db.delete_column('flatcontent_flatcontent', 'site_id')

        # Adding unique constraint on 'FlatContent', fields ['slug']
        db.create_unique('flatcontent_flatcontent', ['slug'])


    models = {
        'flatcontent.flatcontent': {
            'Meta': {'unique_together': "(('slug', 'site'),)", 'object_name': 'FlatContent'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['flatcontent']
