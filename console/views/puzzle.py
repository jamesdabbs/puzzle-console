from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from console.forms import PuzzleForm
from console.models import Puzzle, PuzzleProgress
from console.utils import require_staff, find_team


__all__ = ('edit', 'unlock')


@require_staff
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


@find_team
def unlock(request, game, team, id):
    if request.method == 'POST':
        progress = get_object_or_404(PuzzleProgress, team=team, puzzle__id=id)
        progress.open()
        messages.success(request, 'Puzzle unlocked')
    return redirect('dashboard')
