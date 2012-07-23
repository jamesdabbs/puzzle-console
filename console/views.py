from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse

from .exceptions import TeamBuildingException
from .forms import UserRegistrationForm, PlayerAssignmentForm, TeamUpdateForm
from .models import Team, Player, Game


def home(request):
    """ Renders the homepage """
    return TemplateResponse(request, 'console/base.html', {
        'user_form': UserRegistrationForm(),
        'player_form': PlayerAssignmentForm(),
        'login_form': AuthenticationForm()
    })


def register_player(request):
    """ Allows a user to register and associate a pre-existing Player """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        player_form = PlayerAssignmentForm(request.POST)
        if user_form.is_valid() and player_form.is_valid():
            user = user_form.save()
            player_form.save(user=user)
            messages.success(request, 'New user created.')
            send_mail(
                'APP5 Registration',
                'Thanks for signing up for Auburn Puzzle Party 5: Puzzle Patrol II! \n\n You can use this email address with the password you provided at  registration to log into the Puzzle Console at any time. Players will use the Puzzle Console to manage their Team membership before the event and to access and submit solutions to puzzles during the event. \n\n If you have any questions, feel free to me at steven.clontz@gmail.com. \n\n -Steven',
                'steven.clontz+app5@gmail.com',
                [user.email]
            )
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('teams')
    else:
        user_form = UserRegistrationForm()
        player_form = PlayerAssignmentForm()
    return TemplateResponse(request, 'console/registration/player.html', locals())


def teams(request):
    """ Displays a list of all teams """
    return TemplateResponse(request, 'console/teams/teams.html', {
        'teams': Team.objects.all()
    })


def team_(request, id):
    """ Displays a particular team, and allows its captain to edit it """
    # TODO: A captain currently has no way to abandon a team
    team = get_object_or_404(Team, id=id)
    if request.user == team.captain.user:
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
def claim_team(request, id):
    """ Hook to allow a user to claim an empty, uncaptained team and become
        its captain.
    """
    # TODO: Do we want a similar join team hook or should we leave team
    #       construction to the captains?
    team = get_object_or_404(Team, id=id, captain=None)
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
