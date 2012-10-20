# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PuzzleProgress.difficulty'
        db.add_column('console_puzzleprogress', 'difficulty',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PuzzleProgress.enjoyability'
        db.add_column('console_puzzleprogress', 'enjoyability',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PuzzleProgress.comments'
        db.add_column('console_puzzleprogress', 'comments',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PuzzleProgress.difficulty'
        db.delete_column('console_puzzleprogress', 'difficulty')

        # Deleting field 'PuzzleProgress.enjoyability'
        db.delete_column('console_puzzleprogress', 'enjoyability')

        # Deleting field 'PuzzleProgress.comments'
        db.delete_column('console_puzzleprogress', 'comments')


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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'})
        },
        'console.achievement': {
            'Meta': {'object_name': 'Achievement'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Puzzle']", 'null': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'achievements'", 'to': "orm['console.Team']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'console.clue': {
            'Meta': {'ordering': "['puzzle', 'show_at']", 'object_name': 'Clue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'puzzle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clues'", 'to': "orm['console.Puzzle']"}),
            'show_at': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'console.game': {
            'Meta': {'object_name': 'Game'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rules': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'console.membership': {
            'Meta': {'unique_together': "(('game', 'player', 'team'),)", 'object_name': 'Membership'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Team']", 'null': 'True', 'blank': 'True'})
        },
        'console.player': {
            'Meta': {'ordering': "['name']", 'object_name': 'Player'},
            'games': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['console.Game']", 'through': "orm['console.Membership']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'organizations': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'plays': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'console.puzzle': {
            'Meta': {'ordering': "('game', 'number')", 'unique_together': "(('game', 'number'),)", 'object_name': 'Puzzle'},
            'attachment_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'base_points': ('django.db.models.fields.IntegerField', [], {'default': '500'}),
            'close': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['console.UniqueRandom']", 'unique': 'True'}),
            'completion': ('django.db.models.fields.CharField', [], {'default': "'pr'", 'max_length': '2'}),
            'decay_rate': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'designers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'puzzles_designed'", 'symmetrical': 'False', 'to': "orm['console.Player']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'puzzles'", 'to': "orm['console.Game']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'open': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'playtesters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'puzzles_playtested'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['console.Player']"}),
            'solution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'solution_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'console.puzzleprogress': {
            'Meta': {'object_name': 'PuzzleProgress'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'difficulty': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'enjoyability': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'puzzle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Puzzle']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Team']"}),
            'time_opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_solved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'console.team': {
            'Meta': {'ordering': "['number']", 'unique_together': "(('game', 'name'),)", 'object_name': 'Team'},
            'captain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Player']", 'null': 'True', 'blank': 'True'}),
            'competitive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': "orm['console.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'puzzles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['console.Puzzle']", 'through': "orm['console.PuzzleProgress']", 'symmetrical': 'False'}),
            'staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'console.uniquerandom': {
            'Meta': {'object_name': 'UniqueRandom'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'console.video': {
            'Meta': {'object_name': 'Video'},
            'close': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['console.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'open': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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