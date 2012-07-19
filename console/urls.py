from django.conf.urls import patterns, url

urlpatterns = patterns('console.views',
    url(r'^$', 'home', name='home'),
    url(r'^register/$', 'register_captain', name='register_captain'),
    url(r'^register/team/$', 'register_team', name='register_team')
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout')
)