from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from console.models import Game, Player, Membership
from console.utils import require_staff


__all__ = ('join', 'staff_overview', 'rules', 'about')


@login_required
def join(request, id=None):
    """ Joins the Game without specifying a team (adding the user to the pool
        of interested players)
    """
    game = get_object_or_404(Game, id=id) if id else Game.current()
    player = get_object_or_404(Player, user=request.user)
    Membership.objects.get_or_create(game=game, player=player)
    return redirect('teams')


@require_staff
def staff_overview(request, game, team, id):
    return TemplateResponse(request, 'console/staff/overview.html', {
        'players': Player.objects.all(),
    })


def rules(request):
    return TemplateResponse(request, 'console/game/rules.html')


def about(request):
    return TemplateResponse(request, 'console/game/about.html')


@require_staff
def scoreboard(request, game, team):
    results = {}
    for t in game.teams.all():
        team_results = {}
        for a in t.achievements.filter(points__gte=0):
            hour = int((a.time - game.start).total_seconds() / (60 * 60))
            if hour in team_results:
                team_results[hour] += a.points
            else:
                team_results[hour] = a.points
        results[team] = team_results

    return TemplateResponse(request, 'console/game/scoreboard.html', {
        'results': results
    })
