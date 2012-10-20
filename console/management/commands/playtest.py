from datetime import timedelta
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from console.models import Game, Membership
from console.scripts import verify_puzzle_progresses


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-d', '--duration', dest='duration', default=1, type='int',
            help='Number of hours to condense the playtest to'),
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
            # Grab the old start / stop time
            start = game.start
            stop = game.end
            game.save()

            new_start = now()

            def to_playtest_time(time):
                old_duration = (stop - start).total_seconds()
                new_duration = options.get('duration', 1) * 60 * 60
                progress = float((time - start).total_seconds()) / old_duration
                return new_start + timedelta(seconds=progress * new_duration)

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

            print "\nCopying puzzles ----------------------------------"
            for puzzle in puzzles:
                clues = list(puzzle.clues.all())
                code = puzzle.code
                code.pk = None
                code.save()
                puzzle.game = game
                puzzle.code = code
                puzzle.open = to_playtest_time(puzzle.open)
                puzzle.close = to_playtest_time(puzzle.close)
                puzzle.pk = None
                puzzle.save()
                print "\n"
                print puzzle
                print "\nHints:"
                for clue in clues:
                    clue.puzzle = puzzle
                    clue.pk = None
                    clue.save()
                    print "  @ %s: %s" % (clue.show_at, clue.text)
                print ""

            print "\nCopying videos -----------------------------------"
            for video in videos:
                video.game = game
                video.open = to_playtest_time(video.open)
                video.close = to_playtest_time(video.close)
                video.pk = None
                video.save()
                print video

            print "\nInitializing team progress trackers --------------"
            verify_puzzle_progresses(game)

            print "\nNew default game %s created with id %s" % (game, game.id)
            print "Game will be open from %s to %s\n" % (new_start,
                new_start + timedelta(hours=options.get('duration', 1)))
