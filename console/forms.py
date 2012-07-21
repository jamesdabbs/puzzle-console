import json
from django import forms
from django.contrib.auth.forms import UserCreationForm

from console.models import Player, Team


class UserRegistrationForm(UserCreationForm):
    username = forms.EmailField(label='Email', max_length=75,
        help_text = 'This will double as your username')

    def save(self, player_id=None, player_name=''):
        """ Saves the User as usual, but also adds their email address """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = user.username
        user.save()

        # Fetch / create / update a Player object as well
        if player_id:
            player = Player.objects.get(id=player_id)
        else:
            player = Player(name=player_name)
        player.user = user
        player.save()

        return user


class PlayerAssignmentForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(PlayerAssignmentForm, self).__init__(*args, **kwargs)
        self.choices = json.dumps([p.name for p in Player.objects.all()])


class TeamRegistrationForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.filter(user=None), required=False)

    class Meta:
        model = Team
        sequence = ('name', 'competitive', 'captain')