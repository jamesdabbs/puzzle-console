from collections import Counter
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
        """ Gets the currently active / default game """
        # TODO: add support for multiple active games
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
        """ Returns the players on this team """
        return Player.objects.filter(membership__team=self)
    
    @property
    def player_count(self):
        """ Returns the number of players on this team """
        return Player.objects.filter(membership__team=self).count()
    
    @property
    def player_remaining_count(self):
        """ Returns the number of players allowed to be added to this team """
        return 8 - self.player_count
    
    @property
    def legend_count(self):
        """ Returns the number of Legends on this team """
        return Player.objects.filter(membership__team=self,wins__gte=2).count()
        
    @property
    def allowed_legend_count(self):
        """ Returns how many legends can be on this team if competitive based on how many rookies are on the team """
        rookie_count = Player.objects.filter(membership__team=self,wins=0).count()
        if rookie_count < 2:
            return 2
        elif rookie_count < 4:
            return 3
        else:
            return 4
    
    @property
    def legend_remaining_count(self):
        """ Returns the number of Legends allowed to be added to this team """
        return self.allowed_legend_count - self.legend_count

    def available_players(self):
        """ Returns the players this team could recruit - that is, players not
            on any competing team.
        """
        # TODO: should we also filter out people with no team who have created
        #       User accounts?
        competitors = Team.objects.filter(game=self.game).exclude(id=self.id)
        return Player.objects.exclude(membership__team__in=competitors)

    def assign(self, players, commit=True):
        """ Sets the team players to exactly the given list of players if the
            resulting team would be legal, and throws a TeamBuildingException
            otherwise.
        """
        if not self.captain:
            raise TeamBuildingException('Please assign a captain')
        if self.captain not in players:
            raise TeamBuildingException(
                'You cannot remove the team captain - {}.'.format(self.captain))
        # TODO: swappable backend for validating teams
        if self.competitive:
            if len(players) > 8:
                raise TeamBuildingException('Sorry, competitive teams cannot have more than eight players.')
            counts = Counter(p.status() for p in players)
            rookies, legends = counts['R'], counts['L']
            if legends > 4:
                raise TeamBuildingException(
                    'Sorry, competitive teams cannot have {} Legends.'.format(legends)
                )
            elif rookies < 2*legends - 4:
                raise TeamBuildingException(
                    'Sorry, competitive teams cannot have {} Legends without also having at least {} Rookies.'.format(legends, 2*legends-4)
                )
        if commit:
            # This just flushes and re-adds the members
            # If we start tracking timestamps or anything extra on Membership,
            #   this may need to leave existing members in place
            Membership.objects.filter(team=self).delete()
            Membership.objects.bulk_create([Membership(team=self,
                game=self.game, player=p) for p in players])


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

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.description)

    @property
    def description(self):
        """ Displays a prettified description of the Player's type """
        return {
            0: 'Rookie',
            1: 'Hero'
        }.get(self.wins, 'Legend - %s wins' % self.wins)

    def status(self):
        """ Determines the Players' status, as it pertains to team building """
        return {
            0: 'R',
            1: 'H'
        }.get(self.wins, 'L')  # This method is used in counting the number of
                               # Legends on a team and needs to assign the same
                               # code to all Legends (unlike `description`)

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

    def save(self, *args, **kwargs):
        """ Sets `game` based off `team` (note that `game` is not redundant
            though, since a Player may be signed up for a Game but not yet on a
            particular Team).
        """
        if self.team and not self.game:
            self.game = self.team.game
        super(Membership, self).save(*args, **kwargs)