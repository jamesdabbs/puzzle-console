from django.db import models
from django.template.defaultfilters import timeuntil
from django.utils.timezone import now

from .puzzle import Puzzle


class PuzzleProgress(models.Model):
    UNOPENED = 'U'
    OPENED = 'O'
    SOLVED = 'S'
    FAILED = 'F'
    STATUS_CHOICES = (
        (UNOPENED, 'Unlocked'),
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
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'console'
        verbose_name_plural = 'Puzzle Progresses'

    def __unicode__(self):
        return '%s has %s %s' % (self.team,
            self.get_status_display().lower(), self.puzzle)

    def open(self):
        if (self.status != self.UNOPENED) or not self.puzzle.available():
            raise Puzzle.DoesNotExist
        self.status = self.OPENED
        self.time_opened = now()
        self.save()
        self.team.achievements.create(
            title='Opened "%s"' % self.puzzle.title, time=self.time_opened,
            target=self.puzzle, action='Opened')

    def solve(self):
        if (self.status != self.OPENED) or not self.puzzle.available():
            raise Puzzle.DoesNotExist
        self.status = self.SOLVED
        self.time_solved = now()
        self.save()
        points = self.puzzle.base_points + self.puzzle.decay_rate * self.time_remaining()[1]
        self.team.achievements.create(
            title='Solved "%s"' % self.puzzle.title, time=self.time_solved,
            target=self.puzzle, action='Solved',
            points=points)

    def time_remaining(self):
        _now = now()
        opened = self.time_opened if self.time_opened else _now
        close = self.puzzle.close
        window = (close - opened).seconds
        remaining = timeuntil(close, _now)
        percentage = (100 * (close - _now).seconds) / window
        return remaining, percentage

    def include_template(self):
        if now() < self.puzzle.open:
            return "console/puzzles/locked.html"
        elif now() > self.puzzle.close and self.status != self.SOLVED:
            return "console/puzzles/failed.html"
        else:
            return "console/puzzles/%s.html" % self.get_status_display().lower()

    def timeline_key(self):
        return self.puzzle.open, 2, self.puzzle.number

    def timeline_template(self):
        return 'console/puzzles/base.html'

    def timeline_anchor(self):
        return 'puzzle-%s' % self.puzzle.number

    def visible_clues(self):
        return self.puzzle.clues.filter(show_at__gte=self.time_remaining()[1])
