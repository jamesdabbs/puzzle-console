from django.contrib.auth.models import User
from django.db import models

from console.exceptions import TeamBuildingException
from console.models import Membership


class Player(models.Model):
    user = models.OneToOneField(User, null=True)
    games = models.ManyToManyField('console.Game', through='console.Membership')

    name = models.CharField(max_length=255, blank=True)

    # Metadata about previous plays
    # This should probably be moved to old game result objects and computed
    #   from that
    plays = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    organizations = models.IntegerField(default=0)
        
    class Meta:
        app_label = 'console'
        ordering = ['name']

    def __unicode__(self):
        if self.is_claimed:
            return "%s (%s) <%s>" % (self.name, self.description, self.email)
        else:
            return "%s (%s)" % (self.name, self.description)

    @property
    def description(self):
        """ Displays a prettified description of the Player's type """
        return {
            0: 'Rookie',
            1: 'Hero'
        }.get(self.wins, 'Legend - %s wins' % self.wins)
    
    @property
    def is_claimed(self):
        return User.objects.filter(player=self).exists()
    
    @property
    def email(self):
        if self.is_claimed:
            return self.user
        else:
            return ''

    def status(self):
        """ Determines the Players' status, as it pertains to team building """
        return {
            0: 'R',
            1: 'H'
        }.get(self.wins, 'L')  # This method is used in counting the number of
                               # Legends on a team and needs to assign the same
                               # code to all Legends (unlike `description`)

    def teams(self):
        return self.team_set.all()

    def join(self, team):
        """ Attempts to add this Player to the `team` """
        if self.teams().filter(game=team.game).exists():
            raise TeamBuildingException('You are already a member of a Team.')
        # We can't just .create the Membership, because we want to allow for
        # the possibility of a player who has joined a Game without a Team
        try:
            membership = Membership.objects.get(game=team.game, player=self)
        except Membership.DoesNotExist:
            membership = Membership(game=team.game, player=self)
        membership.team = team
        membership.save()

    def claim(self, team):
        """ Joins the `team` as its captain """
        if team.captain:
            raise TeamBuildingException('This Team already has a captain.')
        # Join the team and assign yourself as captain
        self.join(team)
        team.captain = self
        team.save()