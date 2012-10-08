from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from console.forms import UserRegistrationForm, PlayerAssignmentForm


__all__ = ('register',)

def register(request):
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
            return redirect(request.GET.get('next', 'teams'))
    else:
        user_form = UserRegistrationForm()
        player_form = PlayerAssignmentForm()
    return TemplateResponse(request, 'console/registration/player.html', locals())