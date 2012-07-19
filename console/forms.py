from django import forms
from django.contrib.auth.forms import UserCreationForm

from console.models import Player, Team


class CaptainRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=75)
    player = forms.ModelChoiceField(queryset=Player.objects.filter(user=None),
        empty_label="", required=False)

    def save(self, commit=True):
        # Sets the email attribute on the newly created user
        user = super(CaptainRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        sequence = ('name', 'competitive', 'captain')