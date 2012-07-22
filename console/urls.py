from django.conf.urls import patterns, url

urlpatterns = patterns('console.views',
    url(r'^$', 'home', name='home'),
    url(r'^register/$', 'register_player', name='register_player'),
    url(r'^teams/$', 'teams', name='teams'),
    url(r'^teams/mine/$', 'my_team', name='my_team'),
    url(r'^teams/(?P<id>\d+)/$', 'team_', name='team'),
    url(r'^teams/(?P<id>\d+)/claim/$', 'claim_team', name='claim_team'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login',
        {'template_name': 'console/registration/login.html'}, name='login'),
    url(r'^logout/$', 'logout', name='logout')
)