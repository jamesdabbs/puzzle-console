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
    url(r'^game/join/$', 'join_game', name='join_game'),
    url(r'^staff/(?P<id>\d+)/$', 'game_staff_overview', name='game_staff_overview'),
    url(r'^staff/(?P<game_id>\d+)/puzzle/new$', 'puzzle_edit', name='puzzle_edit'),
    url(r'^staff/(?P<game_id>\d+)/puzzle/(?P<puzzle_id>\d+)$', 'puzzle_edit', name='puzzle_edit'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login',
        {'template_name': 'console/registration/login.html'}, name='login'),
    url(r'^logout/$', 'logout',{'next_page': '/'}, name='logout'),
    url(r'^account/password/reset/$', 'password_reset', {
        'template_name': 'console/registration/password/reset.html',
        'email_template_name': 'console/registration/password/reset_email.html',
    }, name='password_reset'),
    url(r'^account/password/reset/sent/$', 'password_reset_done', {
        'template_name': 'console/registration/password/reset_done.html'}),
    url(r'^account/password/reset/confirm/(?P<uidb36>[-\w]*)/(?P<token>[-\w]*)/$', 
        'password_reset_confirm', 
        {'template_name': 'console/registration/password/reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^account/password/reset/complete/', 'password_reset_complete', 
        {'template_name': 'console/registration/password/reset_complete.html'})
)


urlpatterns += patterns('console.views',
    url(r'^about/', 'about', name='about'),
    url(r'^rules/', 'rules', name='rules'),
)