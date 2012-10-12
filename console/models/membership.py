from django.db import models


class Membership(models.Model):
    game = models.ForeignKey('console.Game')
    player = models.ForeignKey('console.Player')
    team = models.ForeignKey('console.Team', null=True, blank=True)

    class Meta:
        app_label = 'console'
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
