# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WidgetWiring'
        db.delete_table(u'catalogue_widgetwiring')

        # Deleting field 'CatalogueResource.iphone_image_uri'
        db.delete_column(u'catalogue_catalogueresource', 'iphone_image_uri')

        # Deleting field 'CatalogueResource.display_name'
        db.delete_column(u'catalogue_catalogueresource', 'display_name')

        # Deleting field 'CatalogueResource.author'
        db.delete_column(u'catalogue_catalogueresource', 'author')

        # Deleting field 'CatalogueResource.mail'
        db.delete_column(u'catalogue_catalogueresource', 'mail')

        # Deleting field 'CatalogueResource.description'
        db.delete_column(u'catalogue_catalogueresource', 'description')

        # Deleting field 'CatalogueResource.wiki_page_uri'
        db.delete_column(u'catalogue_catalogueresource', 'wiki_page_uri')

        # Deleting field 'CatalogueResource.license'
        db.delete_column(u'catalogue_catalogueresource', 'license')

        # Deleting field 'CatalogueResource.image_uri'
        db.delete_column(u'catalogue_catalogueresource', 'image_uri')

    def backwards(self, orm):
        # Adding model 'WidgetWiring'
        db.create_table(u'catalogue_widgetwiring', (
            ('wiring', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('idResource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.CatalogueResource'])),
            ('friendcode', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'catalogue', ['WidgetWiring'])

        # Adding field 'CatalogueResource.iphone_image_uri'
        db.add_column(u'catalogue_catalogueresource', 'iphone_image_uri',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'CatalogueResource.display_name'
        db.add_column(u'catalogue_catalogueresource', 'display_name',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'CatalogueResource.author'
        raise RuntimeError("Cannot reverse this migration. 'CatalogueResource.author' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'CatalogueResource.author'
        db.add_column(u'catalogue_catalogueresource', 'author',
                      self.gf('django.db.models.fields.CharField')(max_length=250),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'CatalogueResource.mail'
        raise RuntimeError("Cannot reverse this migration. 'CatalogueResource.mail' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'CatalogueResource.mail'
        db.add_column(u'catalogue_catalogueresource', 'mail',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'CatalogueResource.description'
        raise RuntimeError("Cannot reverse this migration. 'CatalogueResource.description' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'CatalogueResource.description'
        db.add_column(u'catalogue_catalogueresource', 'description',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)

        # Adding field 'CatalogueResource.wiki_page_uri'
        db.add_column(u'catalogue_catalogueresource', 'wiki_page_uri',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'CatalogueResource.license'
        db.add_column(u'catalogue_catalogueresource', 'license',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CatalogueResource.image_uri'
        db.add_column(u'catalogue_catalogueresource', 'image_uri',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

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
        'catalogue.catalogueresource': {
            'Meta': {'unique_together': "(('short_name', 'vendor', 'version'),)", 'object_name': 'CatalogueResource'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'uploaded_resources'", 'null': 'True', 'to': "orm['auth.User']"}),
            'fromWGT': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'local_resources'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_description': ('django.db.models.fields.TextField', [], {}),
            'popularity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'template_uri': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'local_resources'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalogue']
