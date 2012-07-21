import json
from console.exceptions import TeamBuildingException
from console.models import Player
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, FormView

from .forms import UserRegistrationForm, PlayerAssignmentForm, \
    TeamRegistrationForm, TeamUpdateForm
from .models import Team


class JsonResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        kwargs['mimetype'] = 'application/json'
        super(JsonResponse, self).__init__(*args, **kwargs)


def home(request):
    return TemplateResponse(request, 'console/base.html', {
        'user_form': UserRegistrationForm(),
        'player_form': PlayerAssignmentForm(),
        'login_form': AuthenticationForm()
    })


# Registration flow
# 1) Create account (either from home or registration page)
# 2) Account must select/create a Player to associate with it
# 3) Once account has a Player, that Player may pick a vacant team to Captain
# 4) Captain selects whether the Team is Competitive or Recreational
# 5) Captain can assigns/create-and-assigns other Players to the Team
# (if the team is Competitive we need to make sure the 8 max and rookie/legend rules are met)
def register_player(request):
    # We may get to this page either by POSTing user data from the homepage
    # or by navigating directly. We'll use a couple of hidden inputs to
    # determine exactly what needs to be handled.
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        player_form = PlayerAssignmentForm(request.POST)
        if user_form.is_valid():
            if 'player_id' in request.POST:
                user = user_form.save(player_id=request.POST['player_id'])
            else:
                user = user_form.save(player_name=request.POST.get('name'))
            messages.success(request, 'New user created')
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('teams')
    else:
        user_form = UserRegistrationForm()
        player_form = PlayerAssignmentForm()
    return TemplateResponse(request, 'console/registration/player.html', locals())


class RegisterTeam(FormView):
    form_class = TeamRegistrationForm
    template_name = 'console/registration/team.html'

    def form_valid(self, form):
        raise NotImplementedError()
register_team = RegisterTeam.as_view()


def teams(request):
    return TemplateResponse(request, 'console/teams/teams.html', {
        'teams': Team.objects.all()
    })


def team(request, id):
    team = get_object_or_404(Team, id=id)
    if request.user.get_profile() == team.captain:
        team_form = TeamUpdateForm(instance=team)
    return TemplateResponse(request, 'console/teams/team.html', locals())


@login_required
def claim_team(request, id):
    team = get_object_or_404(Team, id=id, captain=None)
    player = get_object_or_404(Player, user=request.user)
    try:
        player.claim(team)
    except TeamBuildingException as e:
        messages.error(request, 'Cannot claim team: %s' % e.message)
        return redirect('teams')
    return redirect(team)


def get_player(request):
    name = request.GET.get('name', '')
    players = [dict(d) for d in Player.objects.filter(name__iexact=name).values(
        'id', 'name', 'wins', 'plays', 'organizations')]
    return JsonResponse(json.dumps(players))

# TODO: login next and default locations