from django import forms
from django.contrib.auth.forms import UserCreationForm

from .exceptions import TeamBuildingException
from .models import Player, Team


class UserRegistrationForm(UserCreationForm):
    username = forms.EmailField(label='Email', max_length=75,
        help_text = 'This will double as your username')

    def save(self):
        """ Saves the User as usual, but also adds their email address """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = user.username
        user.save()

        return user


class PlayerAssignmentForm(forms.ModelForm):
    existing_player = forms.ModelChoiceField(
        queryset=Player.objects.filter(user=None),
        required=False
    )
    class Meta:
        model = Player
        fields = ('name',)

    def clean(self):
        data = self.cleaned_data
        old = getattr(data.get('existing_player', None), 'name', '')
        new = data.get('name', '')
        if not (old or new):
            raise forms.ValidationError('Input your name or select an '
                                        'existing player.')
        if old and new and (old.lower() != new.lower()):
            raise forms.ValidationError('Names do not match. (You may leave '
                'the name field blank to use "{}")'.format(old))
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
