# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PuzzleProgress'
        db.create_table('console_puzzleprogress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['console.Team'])),
            ('puzzle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['console.Puzzle'])),
            ('time_opened', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('time_solved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('console', ['PuzzleProgress'])

        # Adding field 'Puzzle.open'
        db.add_column('console_puzzle', 'open',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Puzzle.close'
        db.add_column('console_puzzle', 'close',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


        # Update defaults if needed
        for p in orm.Puzzle.objects.all():
            if p.description is None:
                p.description = ''
                p.save()
            if p.solution is None:
                p.solution = ''
                p.save()
        for g in orm.Game.objects.all():
            if g.about is None:
                g.about = ''
                g.save()
            if g.rules is None:
                g.rules = ''
                g.save()

        # Changing field 'Puzzle.description'
        db.alter_column('console_puzzle', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Puzzle.solution'
        db.alter_column('console_puzzle', 'solution', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Game.about'
        db.alter_column('console_game', 'about', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Game.rules'
        db.alter_column('console_game', 'rules', self.gf('django.db.models.fields.TextField')(default=''))

        # Adding field 'Team.log'
        db.add_column('console_team', 'log',
                      self.gf('console.models.fields.ListField')(default=[]),
                      keep_default=False)

        # Adding field 'Team.extra_points'
        db.add_column('console_team', 'extra_points',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'PuzzleProgress'
        db.delete_table('console_puzzleprogress')

        # Deleting field 'Puzzle.open'
        db.delete_column('console_puzzle', 'open')

        # Deleting field 'Puzzle.close'
        db.delete_column('console_puzzle', 'close')


        # Changing field 'Puzzle.description'
        db.alter_column('console_puzzle', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Puzzle.solution'
        db.alter_column('console_puzzle', 'solution', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Game.about'
        db.alter_column('console_game', 'about', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Game.rules'
        db.alter_column('console_game', 'rules', self.gf('django.db.models.fields.TextField')(null=True))
        # Deleting field 'Team.log'
        db.delete_column('console_team', 'log')

        # Deleting field 'Team.extra_points'
        db.delete_column('console_team', 'extra_points')


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
            'close': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['console.UniqueRandom']", 'unique': 'True'}),
            'completion': ('django.db.models.fields.CharField', [], {'default': "'pr'", 'max_length': '2'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'designers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'puzzles_designed'", 'symmetrical': 'False', 'to': "orm['console.Player']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'open': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'playtesters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'puzzles_playtested'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['console.Player']"}),
            'solution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'console.puzzleprogress': {
            'Meta': {'object_name': 'PuzzleProgress'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'puzzle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Puzzle']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Team']"}),
            'time_opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_solved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'console.team': {
            'Meta': {'ordering': "['number']", 'unique_together': "(('game', 'name'),)", 'object_name': 'Team'},
            'captain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Player']", 'null': 'True', 'blank': 'True'}),
            'competitive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['console.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('console.models.fields.ListField', [], {'default': '[]'}),
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['console']