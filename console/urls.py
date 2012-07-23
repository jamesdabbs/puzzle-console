from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = patterns('console.views',
    url(r'^$', 'home', name='home'),
    url(r'^favicon.ico', RedirectView.as_view(
        url='https://s3.amazonaws.com/app5/favicon.ico', permanent=True)),
    url(r'^register/$', 'register_player', name='register_player'),
    url(r'^teams/$', 'teams_', name='teams'),
    url(r'^teams/mine/$', 'my_team', name='my_team'),
    url(r'^teams/(?P<id>\d+)/$', 'team_', name='team'),
    url(r'^teams/(?P<id>\d+)/claim/$', 'claim_team', name='claim_team'),
    url(r'^game/join/$', 'join_game', name='join_game')
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login',
        {'template_name': 'console/registration/login.html'}, name='login'),
    url(r'^logout/$', 'logout',{'next_page': '/'}, name='logout')
)

urlpatterns += patterns('',
    url(r'^about/', TemplateView.as_view(template_name="console/app5/about.html"), name='about'),
    url(r'^rules/', TemplateView.as_view(template_name="console/app5/rules.html"), name='rules'),
)