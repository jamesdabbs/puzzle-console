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
    registration_form = UserRegistrationForm()
    login_form = AuthenticationForm()
    return TemplateResponse(request, 'console/base.html', locals())


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
            # We only want to redirect if we've handled the
            # PlayerAssignmentForm (or at least, had an opportunity to)
    else:
        user_form = UserRegistrationForm()

    if 'add_player' in request.POST:
        player_form = PlayerAssignmentForm(request.POST, user=request.user)
        if player_form.is_valid():
            player_form.save()
            return redirect('teams')
    else:
        player_form = PlayerAssignmentForm()

    return TemplateResponse(request, 'console/registration/captain.html', locals())


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


@login_required
def claim_team(request, id):
    team = get_object_or_404(Team, id=id, captain=None)
    player = get_object_or_404(Player, user=request.user)
    team.captain = player
    team.save()
    return redirect(team)