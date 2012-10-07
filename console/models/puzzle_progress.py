from django.db import models

class PuzzleProgress(models.Model):
    INVISIBLE = 'I'
    LOCKED = 'L'
    UNLOCKED = 'U'
    OPENED = 'O'
    SOLVED = 'S'
    FAILED = 'F'
    STATUS_CHOICES = (
        (INVISIBLE, 'Invisible'),
        (LOCKED, 'Locked'),
        (UNLOCKED, 'Unlocked'),
        (OPENED, 'Opened'),
        (SOLVED, 'Solved'),
        (FAILED, 'Failed')
    )

    team = models.ForeignKey('console.Team')
    puzzle = models.ForeignKey('console.Puzzle')
    points = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    log = models.TextField()

    class Meta:
        app_label = 'console'