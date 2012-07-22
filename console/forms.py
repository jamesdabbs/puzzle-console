from django import forms
from django.contrib.auth.forms import UserCreationForm

from .exceptions import TeamBuildingException
from .models import Player, Team


class UserRegistrationForm(UserCreationForm):
    username = forms.EmailField(label='Email', max_length=75)

    def save(self):
        """ Saves the User as usual, but also adds their email address """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = user.username
        user.save()

        return user


class PlayerAssignmentForm(forms.ModelForm):
    existing_player = forms.ModelChoiceField(
        queryset=Player.objects.filter(user=None),
        required=False,
        label = "Existing Player"
    )
    name = forms.CharField(
        max_length=255,
        label="New Player",
        required=False
    )
    
    class Meta:
        model = Player
        fields = ('existing_player', 'name')

    def clean(self):
        data = self.cleaned_data
        old = getattr(data.get('existing_player', None), 'name', '')
        new = data.get('name', '')
        if not (old or new):
            raise forms.ValidationError('Please either select an existing player or tell us your name.')
        if old and new and (old.lower() != new.lower()):
            raise forms.ValidationError('You cannot both select an existing player and write a name for a new player.'.format(old))
        return data


    def save(self, user):
        player = self.cleaned_data.get('existing_player', None)
        if not player:
            player = Player(name=self.cleaned_data.get('name'))
        player.user = user
        player.save()



class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'competitive')

    def __init__(self, *args, **kwargs):
        super(TeamUpdateForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['players'] = forms.ModelMultipleChoiceField(
                queryset=self.instance.available_players(),
                initial=self.instance.players()
            )

    def clean(self):
        data = self.cleaned_data
        team, players = self.instance, data.get('players', [])
        try:
            team.assign(players, commit=False)
        except TeamBuildingException as e:
            raise forms.ValidationError(e.message)
        return data

    def save(self):
        team = super(TeamUpdateForm, self).save()
        team.assign(self.cleaned_data.get('players', []))
        return team
