from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from console.models import Game, Player, Puzzle, Membership
from console.utils import check_staff

@login_required
def join_game(request, id=None):
    """ Joins the Game without specifying a team (adding the user to the pool
        of interested players)
    """
    game = get_object_or_404(Game, id=id) if id else Game.current()
    player = get_object_or_404(Player, user=request.user)
    Membership.objects.get_or_create(game=game, player=player)
    return redirect('teams')

@login_required
def game_staff_overview(request, id):
    game = get_object_or_404(Game, id=id)
    if not check_staff(request.user, game):
        raise Http404
    puzzles = Puzzle.objects.filter(game=game)
    players = Player.objects.all()
    return TemplateResponse(request, 'console/staff/overview.html', locals())

def rules(request):
    game = Game.current()
    rules = game.rules
    return TemplateResponse(request, 'console/game/rules.html', locals())

def about(request):
    game = Game.current()
    about = game.about
    return TemplateResponse(request, 'console/game/about.html', locals())
