from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from console.exceptions import TeamBuildingException
from console.forms import TeamUpdateForm
from console.models import Game, Membership, Team


def teams_(request):
    """ Displays a list of all teams """
    game = Game.current()
    teams = Team.objects.filter(game=game, staff=False)
    staff_teams = Team.objects.filter(game=game, staff=True)
    joined = request.user.is_authenticated() and Membership.objects.filter(
        player__user=request.user, game=game).exists()
    return TemplateResponse(request, 'console/teams/teams.html', locals())


def team_(request, id):
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


@login_required
def my_team(request):
    """ Redirects a Player to their Team (if possible, to all teams if not) """
    game = Game.current()
    try:
        return redirect(Team.objects.get(
            membership__player=request.user.get_profile(),
            membership__game=game)
        )
    except Team.DoesNotExist:
        messages.error(request,
            'You have not yet joined a team for {}'.format(game))
        return redirect('teams')


@login_required
def dashboard(request):
    game = Game.current()
    try:
        team = Team.objects.get(
            membership__player__user=request.user,
            membership__game=game)
        )
        return TemplateResponse(request, 'console/team/dashboard.html', locals())
    except Team.DoesNotExist:
        messages.error(request,
            'You have not yet joined a team for {}'.format(game))
        return redirect('teams')
