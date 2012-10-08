from .game import *
from .player import *
from .puzzle import *
from .team import *

from longerusername.forms import AuthenticationForm
from console.forms import UserRegistrationForm, PlayerAssignmentForm


def home(request):
    """ Renders the homepage """
    return TemplateResponse(request, 'console/base.html', {
        'user_form': UserRegistrationForm(),
        'player_form': PlayerAssignmentForm(),
        'login_form': AuthenticationForm()
    })