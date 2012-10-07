from django.db import models


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
    designers = models.ManyToManyField('console.Player', 
        related_name='puzzles_designed')
    playtesters = models.ManyToManyField('console.Player', 
        related_name='puzzles_playtested', null=True, blank=True)
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    attachment_url = models.URLField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)
    completion = models.CharField(max_length=2, default=PROPOSAL, 
        choices=COMPLETION_CHOICES)
    code = models.OneToOneField('console.UniqueRandom')
    
    class Meta:
        app_label = 'console'
        ordering = ['game', 'number']
        unique_together = (("game", "number"),)
    
    def __unicode__(self):
        return self.title