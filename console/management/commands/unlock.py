from optparse import make_option

from django.core.management.base import BaseCommand

from console.models import Game, PuzzleProgress


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--number', dest='number', default=None, type='int',
            help='Lookup by number'),
        make_option('--name', dest='name', default=None, type='str',
            help='Lookup by name (case insensitive)')
    )

    def handle(self, *args, **options):
        game = Game.current()
        number, name = options.get('number'), options.get('name')
        if number:
            print "Unlocking %s ..." % number
            team = game.teams.get(number=number)
        elif name:
            print "Unlocking %s ... " % name
            team = game.teams.get(name__iexact=name)
        else:
            raise ValueError('You must provide a number or name')

        for puzzle in game.puzzles.all():
            print PuzzleProgress.objects.get_or_create(puzzle=puzzle,
                team=team)[0]
        print "Done\n"
