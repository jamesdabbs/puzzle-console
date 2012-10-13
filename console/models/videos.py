from django.db import models


class Video(models.Model):
    game = models.ForeignKey('console.Game', related_name='videos')
    url = models.URLField(blank=True)
    open = models.DateTimeField(null=True, blank=True)
    close = models.DateTimeField(null=True, blank=True)
    number = models.IntegerField()

    class Meta:
        app_label = 'console'

    def __unicode__(self):
        return self.url

    def timeline_key(self):
        return self.open, self.number

    def timeline_template(self):
        raise NotImplementedError

    def timeline_anchor(self):
        return "video-%s" % self.number
