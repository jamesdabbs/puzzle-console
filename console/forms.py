from django import forms
from django.contrib.auth.forms import UserCreationForm

from console.models import Player, Team


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=75)

    def save(self):
        """ Saves the User as usual, but also adds their email address """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        user.save()
        return user


class PlayerAssignmentForm(forms.Form):
    player = forms.ModelChoiceField(queryset=Player.objects.filter(user=None),
        empty_label="", required=False)

    def save(self, user):
        player = self.cleaned_data.get('player')
        if player:
            player.user = user
            player.save()


class TeamRegistrationForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.filter(user=None), required=False)

    class Meta:
        model = Team
        sequence = ('name', 'competitive', 'captain')