from datetime import datetime
from django.db import models


class PuzzleProgress(models.Model):
    CLOSED = 'C'
    OPENED = 'O'
    SOLVED = 'S'
    FAILED = 'F'
    STATUS_CHOICES = (
        (CLOSED, 'Closed'),
        (OPENED, 'Opened'),
        (SOLVED, 'Solved'),
        (FAILED, 'Failed')
    )

    team = models.ForeignKey('console.Team')
    puzzle = models.ForeignKey('console.Puzzle')
    status = models.CharField(max_length=1, default=CLOSED)
    time_opened = models.DateTimeField(null=True, blank=True)
    time_solved = models.DateTimeField(null=True, blank=True)
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'console'
        verbose_name_plural = 'Puzzle Progresses'

    def open(self):
        if (self.status != self.CLOSED) or not self.puzzle.available():
            return
        self.status = self.OPENED
        self.time_opened = datetime.now()
        self.team.log.append(
            'Opened "%s" @ %s.' %
            (self.puzzle.name, self.time_opened))
        self.save()

    def solve(self):
        if (self.status != self.OPENED) or not self.puzzle.available():
            return
        self.status = self.SOLVED
        self.points = points = 500 + 1000 * self.time_remaining()
        self.team.log.append(
            'Solved "%s" @ %s. %s points' %
            (self.puzzle.name, datetime.now(), points))
        self.save()

    def time_remaining(self):
        now = datetime.now()
        opened = self.time_opened if self.time_opened else now
        window = (self.puzzle.close - opened).seconds
        remaining = (self.puzzle.close - now).seconds
        return (100 * remaining) / window
