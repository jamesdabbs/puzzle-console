from django.db import models


class Clue(models.Model):
    puzzle = models.ForeignKey('console.Puzzle', related_name='clues')
    show_at = models.IntegerField()
    text = models.TextField()

    class Meta:
        app_label = 'console'
        ordering = ['puzzle', 'show_at']
