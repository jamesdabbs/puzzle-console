from console.models import Game


def current_game(request):
    # TODO: use this instead of passing game in from views
    return {'current_game': Game.current()}
