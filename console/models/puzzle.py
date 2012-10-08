from datetime import datetime

from django.db import models

from console.utils import generate_code


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

    game = models.ForeignKey('console.Game')
    number = models.IntegerField()
    open = models.DateTimeField()
    close = models.DateTimeField()

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    attachment_url = models.URLField(blank=True)
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

    def save(self, *args, **kwargs):
        if not self.solution_code:
            self.solution_code = generate_code()
        super(Puzzle, self).save(*args, **kwargs)

    def available(self):
        self.open <= datetime.now() <= self.close