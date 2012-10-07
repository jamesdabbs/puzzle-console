from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.http import Http404

from .exceptions import TeamBuildingException
from .forms import UserRegistrationForm, PlayerAssignmentForm, TeamUpdateForm, PuzzleForm
from .models import Team, Player, Game, Puzzle, Membership

from .utils import check_staff