from django.db import models

from console.exceptions import TeamBuildingException
from console.models import Game, Membership, Player


class Team(models.Model):
    game = models.ForeignKey('console.Game')
    captain = models.ForeignKey('console.Player', null=True, blank=True)

    name = models.CharField(max_length=255)
    competitive = models.BooleanField()

    number = models.IntegerField(default=0)

    staff = models.BooleanField(default=False) #Set to True for staffers so that they can see admin tools

    class Meta:
        app_label = 'console'
        ordering = ['number']
        unique_together = (('game', 'name'))

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'team', (), {'id': self.id}

    def save(self, *args, **kwargs):
        """ Sets the default Game, if needed """
        if not self.game:
            self.game = Game.current()
        if self.number == 0:
            top_team = Team.objects.filter(game=self.game).order_by('-number')[0]
            self.number = top_team.number + 1
        super(Team, self).save(*args, **kwargs)

    @property
    def players(self):
        """ Gets the players on this team """
        return Player.objects.filter(membership__team=self)

    @property
    def rookies(self):
        """ Gets players on the team that are Rookies (0 wins) """
        return self.players.filter(wins=0)

    @property
    def legends(self):
        """ Gets the players on the team that are Legends (>1 win) """
        return self.players.filter(wins__gte=2)

    def player_cap(self):
        return 8

    def player_slots(self):
        return self.player_cap() - self.players.count()

    def legend_cap(self):
        return min(self.rookies.count()/2 + 2, 4)

    def legend_slots(self):
        return self.legend_cap() - self.legends.count()

    def available_players(self):
        """ Returns the players this team could recruit - that is, players not
            on any competing team.
        """
        # TODO: should we also filter out people with no team who have created
        #       User accounts?
        competitors = Team.objects.filter(game=self.game).exclude(id=self.id)
        return Player.objects.exclude(membership__team__in=competitors)

    def assign(self, roster, commit=True):
        """ Sets the team players to exactly the given list of players if the
            resulting team would be legal, and throws a TeamBuildingException
            otherwise.
        """
        if not self.captain:
            raise TeamBuildingException('Please assign a captain.')
        if self.captain not in roster:
            raise TeamBuildingException(
                'You cannot remove the team captain - {}.'.format(self.captain))
        # TODO: swappable backend for validating teams
        if self.competitive:
            if len(roster) > 8:
                raise TeamBuildingException('Sorry, competitive teams cannot have more than eight players.')
            rookies, legends = self.rookies.count(), self.legends.count()
            if legends > 4:
                raise TeamBuildingException(
                    'Sorry, competitive teams cannot have {} Legends.'.format(legends)
                )
            elif rookies < 2*legends - 4:
                raise TeamBuildingException(
                    'Sorry, competitive teams cannot have {} Legends without also having at least {} Rookies.'.format(legends, 2*legends-4)
                )
        if commit:
            # We want to add the added players and remove the removed ones
            # without changing the membership of old players that are staying

            # Remove players from the team that aren't on the new roster
            Membership.objects.filter(team=self).exclude(
                player__in=roster).update(team=None)
            # And add the new ones
            for player in roster:
                if player not in self.players:
                    player.join(self)
