from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from console.forms import PuzzleForm
from console.models import  Puzzle
from console.utils import find_team


__all__ = ('edit',)


@find_team(require_staff=True)
def edit(request, game, team, id=None):
    if request.method == 'POST':
        form = PuzzleForm(request.POST)
        if form.is_valid() and form.puzzle.game == game:
            form.save()
    elif id is None:
        form = PuzzleForm()
    else:
        form = PuzzleForm(instance=get_object_or_404(Puzzle, game=game, id=id))
    return TemplateResponse(request, 'console/staff/puzzle.html', locals())
