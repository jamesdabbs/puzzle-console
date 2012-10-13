from datetime import timedelta
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from console.models import Game, Membership
from console.scripts import verify_puzzle_progresses


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-d', '--days', dest='days', default=2, type='int',
            help='Number of days to open playtest puzzles for'),
        make_option('-f', '--finished', dest='finished', action='store_true',
            help='If set, removes the playtest game and restores the original')
    )

    def handle(self, *args, **options):
        print ""
        if options.get('finished', False):
            playtests = Game.objects.filter(name__contains=' (PLAYTEST)')
            count = playtests.count()
            playtests.all().delete()
            game = Game.current()
            if count > 1:
                print "Deleted %s playtest games" % count
            elif count == 1:
                print "Deleted playtest game"
            else:
                print "No active playtests found"
            print "Current game is now %s (id %s)\n" % (game, game.id)

        else:
            game = Game.current()
            print "Creating a new game based on %s" % game
            print "===================================================="
            teams = list(game.teams.filter(staff=True))
            puzzles = list(game.puzzles.all())
            videos = list(game.videos.all())
            game.name += ' (PLAYTEST)'
            game.pk = None
            game.save()

            print "\nCopying staff teams ------------------------------"
            for team in teams:
                players = list(team.players.all())
                team.pk = None
                team.game = game
                team.save()
                print "%s ..." % team,

                for p in players:
                    Membership.objects.create(game=game, player=p, team=team)
                print "%s players" % len(players)

            open = now()
            close = open + timedelta(days=options.get('days', 2))
            print "\nCopying puzzles ----------------------------------"
            for puzzle in puzzles:
                code = puzzle.code
                code.pk = None
                code.save()
                puzzle.game = game
                puzzle.code = code
                puzzle.open = open
                puzzle.close = close
                puzzle.pk = None
                puzzle.save()
                print puzzle

            print "\nCopying videos -----------------------------------"
            for video in videos:
                video.game = game
                video.pk = None
                video.save()
                print video

            print "\nInitializing team progress trackers --------------"
            verify_puzzle_progresses(game)

            print "\nNew default game %s created with id %s" % (game, game.id)
            print "Game will be open from %s to %s\n" % (open, close)
