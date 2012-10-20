from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from console.models import Game, Player, Membership, Achievement
from console.utils import require_staff, JsonResponse


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
    start = min(p.open for p in game.puzzles.all())
    stop = min(p.close for p in game.puzzles.all())

    teams = game.teams.all()
    headers, rows = [''] + [t.name for t in teams], []

    step = start
    while step < stop:
        rows.append([step] + [t.points(before=step) for t in teams])
        step += timedelta(hours=1)

    total = [stop] + [t.points() for t in teams]

    return TemplateResponse(request, 'console/game/scoreboard.html', {
        'headers': headers,
        'rows': rows,
        'total': total
    })


@require_staff
def scoreboard_dump(request, game, team):
    return JsonResponse([{
        'title': a.title,
        'message': a.message,
        'points': a.points,
        'time': a.time.strftime("%d %H:%M:%S"),
        'target': getattr(a.target, 'id', None),
        'action': a.action,
        'team': a.team.number
    } for a in Achievement.objects.filter(team__game=game)])
