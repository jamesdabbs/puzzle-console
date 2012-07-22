from django.contrib.auth.models import User
from django.db import models

from .exceptions import TeamBuildingException


class Game(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def current(cls):
        return Game.objects.get(name='Puzzle Patrol II')


class Team(models.Model):
    game = models.ForeignKey(Game,default=Game.current().id)
    captain = models.ForeignKey('Player', null=True, blank=True)

    name = models.CharField(max_length=255)
    competitive = models.BooleanField()

    class Meta:
        unique_together = (('game', 'name'),)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'team', (), {'id': self.id}

    def players(self):
        return Player.objects.filter(membership__team=self)

    def available_players(self):
        competitors = Team.objects.filter(game=self.game).exclude(id=self.id)
        return Player.objects.exclude(membership__team__in=competitors)


class Player(models.Model):
    # A Player may or may not have a User attached. If not, the player may be
    # assigned to a Team by that Team's captain
    user = models.OneToOneField(User, null=True)
    games = models.ManyToManyField(Game, through='Membership')

    name = models.CharField(max_length=255, blank=True)

    # Metadata about previous plays
    # This should probably be moved to old game result objects and computed
    #   from that
    plays = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    organizations = models.IntegerField(default=0)

    @property
    def description(self):
        """ Displays a prettified description of the Player's type
        """
        # Puzzle Patrol II specific
        return {
            0: 'Rookie',
            1: 'Hero'
        }.get(self.wins, 'Legend - %s wins' % self.wins)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.description)

    def teams(self):
        """ All teams that this Player is a member of """
        return Team.objects.filter(membership__player=self)

    def join(self, team):
        """ Attempts to add this Player to the `team` """
        if self.teams().filter(game=team.game).exists():
            raise TeamBuildingException('You may only join one team per game')
        Membership.objects.create(team=team, game=team.game, player=self)

    def claim(self, team):
        """ Joins the `team` as its captain """
        if team.captain:
            raise TeamBuildingException('This team already has a captain')
        # Join the team and assign yourself as captain
        self.join(team)
        team.captain = self
        team.save()


class Membership(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team, null=True)

    class Meta:
        # A player can only be on one team per game
        unique_together = (('game', 'player', 'team'),)

