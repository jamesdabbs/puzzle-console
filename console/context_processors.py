from console.models import Game

def current_game(request):
    return {'current_game': Game.current()}