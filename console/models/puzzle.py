from django.db import models
from django.utils.timezone import now


class Puzzle(models.Model):
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

    game = models.ForeignKey('console.Game', related_name='puzzles')
    number = models.IntegerField()
    open = models.DateTimeField(null=True, blank=True)
    close = models.DateTimeField(null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    locked_description = models.TextField(blank=True)
    attachment_url = models.URLField(null=True, blank=True)
    solution = models.TextField(blank=True)
    code = models.OneToOneField('console.UniqueRandom')

    designers = models.ManyToManyField('console.Player',
        related_name='puzzles_designed')
    playtesters = models.ManyToManyField('console.Player',
        related_name='puzzles_playtested', null=True, blank=True)
    completion = models.CharField(max_length=2, default=PROPOSAL,
        choices=COMPLETION_CHOICES)

    class Meta:
        app_label = 'console'
        ordering = ('game', 'number')
        unique_together = (("game", "number"),)

    def __unicode__(self):
        return self.title

    def available(self):
        return self.open <= now() <= self.close
