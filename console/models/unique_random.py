# UniqueRandom adapted from https://github.com/workmajj/django-unique-random released under public domain.
from random import randrange

from django.db import models

from console.models import Puzzle


# Example set is Crockford's encoding:
# http://www.crockford.com/wrmg/base32.html
UR_CHARSET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
UR_LENGTH = 6
UR_MAX_TRIES = 2048


class UniqueRandom(models.Model):
    code = models.CharField(max_length=UR_LENGTH, editable=False, unique=True)
    
    class Meta:
        app_label = 'console'
        verbose_name = "Unique Random Code"
        verbose_name_plural = "Unique Random Codes"
    
    def __unicode__(self):
        try:
            return "%s (%s)" % (self.code, self.puzzle)
        except Puzzle.DoesNotExist:
            return self.code
    
    def save(self, *args, **kwargs):
        """
        Upon saving, generate a code by randomly picking LENGTH number of
        characters from CHARSET and concatenating them. If code has already
        been used, repeat until a unique code is found, or fail after trying
        MAX_TRIES number of times. (This will work reliably for even modest
        values of LENGTH and MAX_TRIES, but do check for the exception.)
        Discussion of method: http://stackoverflow.com/questions/2076838/
        """
        unique = False
        for loop in range(0,UR_MAX_TRIES):
            new_code = ''
            for i in xrange(UR_LENGTH):
                new_code += UR_CHARSET[randrange(0, len(UR_CHARSET))]
            if not UniqueRandom.objects.filter(code=new_code):
                self.code = new_code
                unique = True
        if not unique:
            raise ValueError("Error producing unqiue code.")
        super(UniqueRandom, self).save(*args, **kwargs)