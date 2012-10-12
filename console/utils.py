import json

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect

from .models import Game, Team


class JsonResponse(HttpResponse):
    def __init__(self, data):
        super(JsonResponse, self).__init__(
            json.dumps(data), mimetype='application/json')


def _find_team(require_staff=False):
    def decorator(view):
        def _wrapped_view(request, *args, **kwargs):
            game = Game.current()
            try:
                team = game.team_for(request.user)
            except Team.DoesNotExist:
                messages.error(request, 'You must be on a team to participate.')
                return redirect('teams')
            if require_staff and not team.staff:
                raise Http404
            kwargs.update({'game': game, 'team': team})
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator

find_team = _find_team()
require_staff = _find_team(True)
