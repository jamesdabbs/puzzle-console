from django.views.generic import TemplateView, FormView

from .forms import CaptainRegistrationForm, TeamRegistrationForm

# 1) Create account
# 2) Account must select/create a Player to associate with it
# 3) Once account has a Player, that Player may pick a vacant team to Captain
# 4) Captain selects whether the Team is Competitive or Recreational
# 5) Captain can assigns/create-and-assigns other Players to the Team
# (if the team is Competitive we need to make sure the 8 max and rookie/legend rules are met)

class Home(TemplateView):
    template_name = 'console/home.html'
home = Home.as_view()


class RegisterCaptain(FormView):
    form_class = CaptainRegistrationForm
    template_name = 'console/registration/captain.html'

    def form_valid(self, form):
        raise NotImplementedError()
register_captain = RegisterCaptain.as_view()


class RegisterTeam(FormView):
    form_class = TeamRegistrationForm
    template_name = 'console/registration/team.html'

    def form_valid(self, form):
        raise NotImplementedError()
register_team = RegisterTeam.as_view()
