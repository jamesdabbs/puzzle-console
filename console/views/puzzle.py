from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from console.forms import PuzzleForm
from console.models import Puzzle, PuzzleProgress
from console.utils import require_staff, find_team


__all__ = ('edit', 'unlock')


@require_staff
def edit(request, game, team, puzzle_id=None, **kwargs):
    if request.method == 'POST':
        form = PuzzleForm(request.POST)
        if form.is_valid() and form.puzzle.game == game:
            form.save()
    elif puzzle_id is None:
        form = PuzzleForm()
    else:
        form = PuzzleForm(instance=get_object_or_404(Puzzle,
            game=game, id=puzzle_id))
    return TemplateResponse(request, 'console/staff/puzzle.html', locals())


@require_POST
@find_team
def unlock(request, game, team, id):
    progress = get_object_or_404(PuzzleProgress, team=team, puzzle__id=id)
    try:
        progress.open()
        messages.success(request, 'Puzzle unlocked')
    except:
        messages.warning(request, "Couldn't open puzzle. (If it isn't already unlocked, please contact a staff member)")
    return redirect('%s#%s' % (
        reverse('dashboard'), progress.timeline_anchor()))
