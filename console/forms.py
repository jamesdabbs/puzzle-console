from django import forms
from django.contrib.auth.forms import UserCreationForm

from .exceptions import TeamBuildingException
from .models import Player, Team, Puzzle


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
        assert player is None, "Tried to claim existing player during a puzzle party"
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
                initial=self.instance.players,
                label='Existing Players'
            )
            # Also add 'New Player' fields for the creation of new players
            max_length = Player._meta.get_field('name').max_length
            for i in range(1, self.instance.player_cap()):
                field = forms.CharField(
                    label='New Players' if i == 1 else '',
                    max_length=max_length,
                    required=False
                )
                self.fields['new_player_{}'.format(i)] = field

    def new_players(self):
        # TODO: can we hook in the new players with the pre-save form validation?
        #       Imagine a new team saving 3 existing legends and 2 new rookies
        return [v for k,v in self.cleaned_data.items() if v and k.startswith('new_player_')]

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
        # Create the new players
        new_players = [Player.objects.create(name=name) for name in self.new_players()]
        # And assign all the Players to the Team
        players = list(self.cleaned_data.get('players', [])) + new_players
        team.assign(players)
        return team


class PuzzleForm(forms.ModelForm):
    class Meta:
        model = Puzzle
