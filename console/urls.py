from django.conf.urls import patterns, url

urlpatterns = patterns('console.views',
    url(r'^$', 'home', name='home'),
    url(r'^register/$', 'register_player', name='register_player'),
    url(r'^register/team/$', 'register_team', name='register_team'),
    url(r'^teams/$', 'teams', name='teams'),
    url(r'^teams/(?P<id>\d+)/$', 'team', name='team'),
    url(r'^teams/(?P<id>\d+)/claim/$', 'claim_team', name='claim_team'),
    url(r'^player/by_name/$', 'get_player', name='get_player')
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login',
        {'template_name': 'console/registration/login.html'}, name='login'),
    url(r'^logout/$', 'logout', name='logout')
)