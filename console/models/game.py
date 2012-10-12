from django.db import models
from django.utils.timezone import now

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
        default = cls.objects.get(id=18)
        try:
            return cls.objects.get(name=default.name + ' (PLAYTEST)')
        except:
            return default

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
        return self.teams.get(membership__player__user=user)

    def finished(self):
        return not self.puzzles.filter(close__gte=now()).exists()
