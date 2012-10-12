from console.models import Game


def current_game(request):
    return {'game': Game.current()}
