from fabric.api import local


def deploy():
    local('heroku maintenance:on')
    local('git push heroku master')
    local('heroku config:unset DEBUG')
    local('heroku maintenance:off')
