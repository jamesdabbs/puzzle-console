# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table('console_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('console', ['Game'])

        # Adding model 'Team'
        db.create_table('console_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['console.Game'])),
            ('captain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['console.Player'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('competitive', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('console', ['Team'])

        # Adding unique constraint on 'Team', fields ['game', 'name']
        db.create_unique('console_team', ['game_id', 'name'])

        # Adding model 'Player'
        db.create_table('console_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('plays', self.gf('django.db.models.fields.IntegerField')()),
            ('wins', self.gf('django.db.models.fields.IntegerField')()),
            ('organizations', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('console', ['Player'])

        # Adding model 'Membership'
        db.create_table('console_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['console.Game'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['console.Player'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['console.Team'], null=True)),
        ))
        db.send_create_signal('console', ['Membership'])

        # Adding unique constraint on 'Membership', fields ['game', 'player', 'team']
        db.create_unique('console_membership', ['game_id', 'player_id', 'team_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Membership', fields ['game', 'player', 'team']
        db.delete_unique('console_membership', ['game_id', 'player_id', 'team_id'])

        # Removing unique constraint on 'Team', fields ['game', 'name']
        db.delete_unique('console_team', ['game_id', 'name'])

        # Deleting model 'Game'
        db.delete_table('console_game')

        # Deleting model 'Team'
        db.delete_table('console_team')

        # Deleting model 'Player'
        db.delete_table('console_player')

        # Deleting model 'Membership'
        db.delete_table('console_membership')


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
        'console.game': {
            'Meta': {'object_name': 'Game'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'console.membership': {
            'Meta': {'unique_together': "(('game', 'player', 'team'),)", 'object_name': 'Membership'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Team']", 'null': 'True'})
        },
        'console.player': {
            'Meta': {'object_name': 'Player'},
            'games': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['console.Game']", 'through': "orm['console.Membership']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organizations': ('django.db.models.fields.IntegerField', [], {}),
            'plays': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'wins': ('django.db.models.fields.IntegerField', [], {})
        },
        'console.team': {
            'Meta': {'unique_together': "(('game', 'name'),)", 'object_name': 'Team'},
            'captain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Player']", 'null': 'True'}),
            'competitive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['console']