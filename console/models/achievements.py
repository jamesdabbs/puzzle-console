from django.db import models


class Achievement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    points = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey('console.Puzzle', null=True)
    action = models.CharField(max_length=32, blank=True)
    team = models.ForeignKey('console.Team', related_name='achievements')

    class Meta:
        app_label = 'console'

    def __unicode__(self):
        result = '%s @ %s' % (self.title, self.time)
        if self.points:
            result += ' (%s points)' % self.points
        return result
