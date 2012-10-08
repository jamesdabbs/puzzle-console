from random import randrange
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect

from .models import Game, Team


def JsonResponse(HttpResponse):
    raise NotImplementedError
    # TODO

def generate_code(game):
    CHARSET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
    LENGTH = 6
    RETRIES = 2048

    # TODO - one query
    taken = set(p.solution_code for p in game.puzzle_set.all())
    for loop in range(0, RETRIES):
        code = ''
        for i in xrange(LENGTH):
            code += CHARSET[randrange(0, len(CHARSET))]
        if not code in taken:
            return code
    raise ValueError("Failed to produce unique code in %s tries" % RETRIES)


def find_team(require_staff=False):
    def decorator(view):
        def _wrapped_view(request, *args, **kwargs):
            game = Game.current()
            try:
                team = game.team_for(request.user)
            except Team.DoesNotExist:
                messages.error(request, 'You must join a team to participate.')
                return redirect('teams')
            if require_staff and not team.staff:
                raise Http404
            kwargs.update({'game': game, 'team': team})
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator