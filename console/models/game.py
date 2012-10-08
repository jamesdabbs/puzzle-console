from django.db import models

from .player import Player


class Game(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    rules = models.TextField(blank=True)
    about = models.TextField(blank=True)

    class Meta:
        app_label = 'console'

    def __unicode__(self):
        return self.name

    @classmethod
    def current(cls):
        # TODO: add support for multiple active games
        return cls.objects.get(id=18)

    def free_players(self):
        """ Gets Players interested in this Game who have not signed up for a
            particular team.
        """
        return Player.objects.filter(
            membership__game=self, membership__team=None)

    def staffers(self):
        """ Grabs Players on teams which are marked as Staff teams"""
        return Player.objects.filter(
            membership__game=self, membership__team__staff=True)

    def validate(self, team):
        # TODO: validate the team based on the validation rules for this game
        raise NotImplementedError()

    def team_for(self, user):
        return self.team_set.get(membership__player__user=user)