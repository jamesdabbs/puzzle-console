from console.exceptions import TeamBuildingException
from console.models import Player
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, FormView

from .forms import UserRegistrationForm, PlayerAssignmentForm, \
    TeamRegistrationForm
from .models import Team


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
    if 'create_user' in request.POST:
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, 'New user created')
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            # We'll redirect after the 'add_player' form
    else:
        user_form = UserRegistrationForm()

    if 'add_player' in request.POST:
        player_form = PlayerAssignmentForm(request.POST)
        if player_form.is_valid() and request.user.is_authenticated():
            player_form.save(user=request.user)
            # We should redirect if the user has been registered and has at
            # least seen this form. (They need not actually select a Player)
            # TODO: If they don't select an existing player, do we need to
            #       create a blank one? What about merging in an existing one
            #       later?
            return redirect('teams')
    else:
        player_form = PlayerAssignmentForm()

    return TemplateResponse(request, 'console/registration/player.html', locals())


class RegisterTeam(FormView):
    form_class = TeamRegistrationForm
    template_name = 'console/registration/team.html'

    def form_valid(self, form):
        raise NotImplementedError()
register_team = RegisterTeam.as_view()


def teams(request):
    return TemplateResponse(request, 'console/teams.html', {
        'teams': Team.objects.all()
    })


def team(request, id):
    team = get_object_or_404(Team, id=id)
    return TemplateResponse(request, 'console/team.html', locals())


@login_required
def claim_team(request, id):
    team = get_object_or_404(Team, id=id, captain=None)
    player = get_object_or_404(Player, user=request.user)
    try:
        player.claim(team)
    except TeamBuildingException as e:
        messages.error(request, 'Cannot claim team: %s' % e.message)
    return redirect(team)