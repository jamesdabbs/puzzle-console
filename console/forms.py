from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CaptainRegistrationForm(AuthenticationForm):
    pass


class TeamRegistrationForm(forms.Form):
    pass