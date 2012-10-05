from collections import Counter
from django.contrib.auth.models import User
from django.db import models

from .exceptions import TeamBuildingException


class Game(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    rules = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def current(cls):
        """ Gets the currently active / default game """
        # TODO: add support for multiple active games
        return Game.objects.get(id=18)

    def free_players(self):
        """ Gets Players interested in this Game who have not signed up for a
            particular team.
        """
        return Player.objects.filter(
            membership__game=self, membership__team=None)
    
    def staffers(self):
        """ Grabs Players on teams which are marked as Staff teams"""
        return Player.objects.filter(membership__game=self, membership__team__staff=True)


class Team(models.Model):
    game = models.ForeignKey(Game)
    captain = models.ForeignKey('Player', null=True, blank=True)

    name = models.CharField(max_length=255)
    competitive = models.BooleanField()
    
    number = models.IntegerField(default=0)
    
    staff = models.BooleanField(default=False) #Set to True for staffers so that they can see admin tools

    class Meta:
        unique_together = (('game', 'name'))
        ordering = ['number']

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


class Player(models.Model):
    # A Player may or may not have a User attached.
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
        """ All teams that this Player is a member of """
        return Team.objects.filter(membership__player=self)

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
        
    class Meta:
        ordering = ['name']


class Membership(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team, null=True, blank=True)

    class Meta:
        # A player can only be on one team per game
        unique_together = (('game', 'player', 'team'),)
    
    def __unicode__(self):
        return "%s on %s for %s" % (self.player, self.team, self.game)

    def save(self, *args, **kwargs):
        """ Sets `game` based off `team` (note that `game` is not redundant
            though, since a Player may be signed up for a Game but not yet on a
            particular Team).
        """
        if self.team and not self.game:
            self.game = self.team.game
        super(Membership, self).save(*args, **kwargs)


class Puzzle(models.Model):
    game = models.ForeignKey(Game)
    designers = models.ManyToManyField(Player, related_name='puzzles_designed')
    playtesters = models.ManyToManyField(Player, related_name='puzzles_playtested', null=True, blank=True)
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    attachment_url = models.URLField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)
    
    
    PROPOSAL = 'pr'
    DRAFT = 'dr'
    PLAYTEST = 'pl'
    FINALIZING = 'f'
    COMPLETE = 'c'
    COMPLETION_CHOICES = (
        (PROPOSAL, 'Proposal'),
        (DRAFT, 'Draft'),
        (PLAYTEST, 'Playtest'),
        (FINALIZING, 'Finalizing'),
        (COMPLETE, 'Complete'),
    )
    
    completion = models.CharField(max_length=2, default=PROPOSAL, choices=COMPLETION_CHOICES)
    
    code = models.OneToOneField('UniqueRandom')
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['game', 'number']
        unique_together = (("game", "number"),)



# UniqueRandom adapted from https://github.com/workmajj/django-unique-random released under public domain.
from random import randrange

# Example set is Crockford's encoding:
# http://www.crockford.com/wrmg/base32.html
UR_CHARSET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
UR_LENGTH = 6 #original 16
UR_MAX_TRIES = 2048 #original 1024

class UniqueRandom(models.Model):
    
    code = models.CharField(max_length=UR_LENGTH, editable=False, unique=True)
    
    class Meta:
        verbose_name = "Unique Random Code"
        verbose_name_plural = "Unique Random Codes"
    
    def __unicode__(self):
        try:
            return "%s (%s)" % (self.code, self.puzzle)
        except Puzzle.DoesNotExist:
            return self.code
    
    def save(self, *args, **kwargs):
        """
        Upon saving, generate a code by randomly picking LENGTH number of
        characters from CHARSET and concatenating them. If code has already
        been used, repeat until a unique code is found, or fail after trying
        MAX_TRIES number of times. (This will work reliably for even modest
        values of LENGTH and MAX_TRIES, but do check for the exception.)
        Discussion of method: http://stackoverflow.com/questions/2076838/
        """
        loop_num = 0
        unique = False
        for loop in range(0,UR_MAX_TRIES):
            new_code = ''
            for i in xrange(UR_LENGTH):
                new_code += UR_CHARSET[randrange(0, len(UR_CHARSET))]
            if not UniqueRandom.objects.filter(code=new_code):
                self.code = new_code
                unique = True
        if unique == False:
            raise ValueError("Error producing unqiue code.")
        super(UniqueRandom, self).save(*args, **kwargs)