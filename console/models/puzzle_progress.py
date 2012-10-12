from django.db import models
from django.utils.timezone import now


class PuzzleProgress(models.Model):
    UNOPENED = 'U'
    OPENED = 'O'
    SOLVED = 'S'
    FAILED = 'F'
    STATUS_CHOICES = (
        (UNOPENED, 'Unopened'),
        (OPENED, 'Opened'),
        (SOLVED, 'Solved'),
        (FAILED, 'Failed')
    )

    team = models.ForeignKey('console.Team')
    puzzle = models.ForeignKey('console.Puzzle')
    status = models.CharField(max_length=1,
        choices=STATUS_CHOICES, default=UNOPENED)
    time_opened = models.DateTimeField(null=True, blank=True)
    time_solved = models.DateTimeField(null=True, blank=True)
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'console'
        verbose_name_plural = 'Puzzle Progresses'

    def __unicode__(self):
        return '%s has %s %s' % (self.team,
            self.get_status_display().lower(), self.puzzle)

    def open(self):
        if (self.status != self.UNOPENED) or not self.puzzle.available():
            return
        self.status = self.OPENED
        self.time_opened = now()
        self.team.log.append(
            'Opened "%s" @ %s.' %
            (self.puzzle.title, self.time_opened))
        self.save()

    def solve(self):
        if (self.status != self.OPENED) or not self.puzzle.available():
            return
        self.status = self.SOLVED
        self.time_solved = now()
        self.points = points = 500 + 1000 * self.time_remaining()
        self.team.log.append(
            'Solved "%s" @ %s. %s points' %
            (self.puzzle.title, self.time_solved, points))
        self.save()

    def time_remaining(self):
        opened = self.time_opened if self.time_opened else now()
        window = (self.puzzle.close - opened).seconds
        remaining = (self.puzzle.close - now()).seconds
        return (100 * remaining) / window
