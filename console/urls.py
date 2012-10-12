from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

urlpatterns = patterns('console.views',
    url(r'^$', 'home', name='home'),
    url(r'^favicon.ico', RedirectView.as_view(
        url='https://s3.amazonaws.com/app5/favicon.ico', permanent=True)),
)

urlpatterns += patterns('console.views.game',
    url(r'^join/$', 'join', name='join_game'),
    url(r'^about/$', 'about', name='about'),
    url(r'^rules/$', 'rules', name='rules'),
    url(r'^staff/(?P<id>\d+)/$', 'staff_overview', name='staff_overview')
)

urlpatterns += patterns('console.views.player',
    url(r'^register/$', 'register', name='register_player'),
)

urlpatterns += patterns('console.views.puzzle',
    url(r'^staff/(?P<game_id>\d+)/puzzle/new/$', 'edit'),
    url(r'^staff/(?P<game_id>\d+)/puzzle/(?P<puzzle_id>\d+)/$', 'edit', name='puzzle_edit'),
    url(r'^puzzle/(?P<id>\d+)/unlock/$', 'unlock', name='unlock_puzzle')
)

urlpatterns += patterns('console.views.team',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^solve/$', 'solve', name='solve_puzzle'),
    url(r'^teams/$', 'index', name='teams'),
    url(r'^teams/(?P<id>\d+)/$', 'show', name='team'),
    url(r'^teams/(?P<id>\d+)/claim/$', 'claim', name='claim_team'),
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