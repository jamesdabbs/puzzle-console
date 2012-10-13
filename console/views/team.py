from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from console.exceptions import TeamBuildingException
from console.forms import TeamUpdateForm
from console.models import Game, Membership, Player, Team
from console.utils import find_team, JsonResponse


__all__ = ('index', 'show', 'claim', 'dashboard', 'solve')


def index(request):
    """ Displays a list of all teams """
    game = Game.current()
    return TemplateResponse(request, 'console/teams/teams.html', {
        'teams': Team.objects.filter(game=game, staff=False),
        'staff_teams': Team.objects.filter(game=game, staff=True),
        'joined': request.user.is_authenticated() and Membership.objects\
            .filter(player__user=request.user, game=game).exists()
    })


def show(request, id):
    """ Displays a particular team, and allows its captain to edit it """
    # TODO: A captain currently has no way to abandon a team
    team = get_object_or_404(Team, id=id)
    if request.user == getattr(team.captain, 'user', None):
        if request.method == 'POST':
            form = TeamUpdateForm(request.POST, instance=team)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Team updated')
                except (TeamBuildingException, IntegrityError) as e:
                    messages.error(request, 'Error saving team: {}'.format(e))
                return redirect(team)
        else:
            form = TeamUpdateForm(instance=team)

    return TemplateResponse(request, 'console/teams/team.html', locals())


@login_required
def claim(request, id):
    """ Hook to allow a user to claim an empty, uncaptained team and become
        its captain.
    """
    # TODO: Do we want a similar join team hook or should we leave team
    #       construction to the captains?
    team = get_object_or_404(Team, id=id)
    player = get_object_or_404(Player, user=request.user)
    try:
        player.claim(team)
    except TeamBuildingException as e:
        messages.error(request, 'Cannot claim team: %s' % e.message)
        return redirect('teams')
    return redirect(team)


@find_team
def dashboard(request, game, team):
    return TemplateResponse(request, 'console/teams/dashboard.html', locals())


@require_POST
@find_team
def solve(request, game, team):
    code = request.POST.get('code', '')
    if team.solve(code):
        messages.success(request, 'Puzzle solved')
    else:
        messages.error(request, 'Invalid code')
    return redirect('dashboard')
