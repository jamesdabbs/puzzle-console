from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()


class Team(models.Model):
    game = models.ForeignKey(Game)
    captain = models.ForeignKey('Player')

    name = models.CharField(max_length=255)

    class Meta:
        unique_together = (('game', 'name'),)


class Player(models.Model):
    # A Player may or may not have a User attached. If not, the player may be
    # assigned to a Team by that Team's captain
    user = models.ForeignKey(User, null=True)
    games = models.ManyToManyField(Game, through='Membership')

    name = models.CharField(max_length=255)


class Membership(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team, null=True)

