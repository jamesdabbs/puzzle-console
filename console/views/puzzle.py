from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from console.forms import PuzzleForm
from console.models import Game, Puzzle
from console.utils import check_staff


@login_required
def puzzle_edit(request, **kwargs): 
    #did we provide a game id?
    game_id = kwargs.get('game_id', None)
    #if not 404
    if game_id is None:
        raise Http404
    #if this isn't a game 404
    game = get_object_or_404(Game, id=game_id)
    #if user isn't a staffer 404
    if not check_staff(request.user, game):
        raise Http404
    #if POST then submit the form
    if request.method == 'POST':
        form = PuzzleForm(request.POST)
        # only save the form if puzzle matches URL
        if form.is_valid() and form.puzzle.game == game:
            form.save()
    else:
        #did we provide a puzzle id?
        puzzle_id = kwargs.get('puzzle_id', None)
        #if not create new puzzle
        if puzzle_id is None:
            form = PuzzleForm()
        else:
            puzzle = get_object_or_404(Puzzle, id=puzzle_id)
            if game == puzzle.game:
                form = PuzzleForm(instance=puzzle)
            else:
                raise Http404
    return TemplateResponse(request, 'console/staff/puzzle.html', locals())