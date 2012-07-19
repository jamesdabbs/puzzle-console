from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.name


class Team(models.Model):
    game = models.ForeignKey(Game)
    captain = models.ForeignKey('Player', null=True)

    name = models.CharField(max_length=255)
    competitive = models.BooleanField()

    class Meta:
        unique_together = (('game', 'name'),)

    def __unicode__(self):
        return self.name


class Player(models.Model):
    # A Player may or may not have a User attached. If not, the player may be
    # assigned to a Team by that Team's captain
    user = models.ForeignKey(User, null=True)
    games = models.ManyToManyField(Game, through='Membership')

    name = models.CharField(max_length=255)

    # Metadata about previous plays
    # This should probably be moved to old game result objects and computed
    #   from that
    plays = models.IntegerField()
    wins = models.IntegerField()
    organizations = models.IntegerField()

    def __unicode__(self):
        return self.name

    # Meta-data formatting methods for Puzzle Patrol II
    # This should be factored into swappable backend for reuse
    def description(self):
        return {
            0: 'Rookie',
            1: 'Hero'
        }.get(self.wins, 'Legend')


class Membership(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team, null=True)

    class Meta:
        # A player can only be on one team per game
        unique_together = (('game', 'player', 'team'),)

