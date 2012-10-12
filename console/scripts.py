import csv
from datetime import timedelta
import os

from django.utils.timezone import now

from console.models import Game, Player, Team, Membership, PuzzleProgress


DATA_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def add_players():
    # Loads player data from player_data.csv, creating games and players as
    # needed
    with open(os.path.join(DATA_ROOT, 'player_data.csv'), 'r') as f:
        reader = csv.reader(f)

        def get_game(header):
            # Don't worry about the last name / first name columns
            if header in ['Last', 'First']:
                return header
            name = header.split('(')[0].strip()
            game, created = Game.objects.get_or_create(name=name)

            action = 'Created' if created else 'Found'
            print '{} game: {}'.format(action, game)
            return game
        map(get_game, reader.next())

        for row in reader:
            last, first, plays = row[0].strip(), row[1].strip(), row[2:]
            name = '{} {}'.format(first, last)
            try:
                player = Player.objects.get(name=name)
            except Player.DoesNotExist:
                player = Player(name=name)

            # Compute the number of trophies / status
            player.plays = plays.count('P')
            player.wins = plays.count('T')
            player.organizations = plays.count('O')
            player.save()
            print player


def setup_puzzle_patrol_2():
    game, created = Game.objects.get_or_create(name='Puzzle Patrol II')
    action = 'Created' if created else 'Found'
    print '{} game: {}'.format(action, game)

    # Create 10 teams
    teams = Team.objects.filter(game=game).count()
    for i in range(teams, 10):
        print Team.objects.create(name='Team {}'.format(i + 1), game=game)


def playtest_current_game(open_days=1):
    game = Game.current()
    teams = list(game.teams.filter(staff=True))
    puzzles = list(game.puzzles.all())
    game.name += ' (PLAYTEST)'
    game.pk = None
    game.save()

    # Copy the staff teams
    for team in teams:
        players = list(team.players.all())
        team.pk = None
        team.game = game
        print team.save()

        for p in players:
            print Membership.objects.create(game=game, player=p, team=team)

    # Copy the puzzles and set them to open
    open = now()
    close = open + timedelta(days=open_days)
    for puzzle in puzzles:
        code = puzzle.code
        code.pk = None
        code.save()
        puzzle.game = game
        puzzle.code = code
        puzzle.open = open
        puzzle.close = close
        puzzle.pk = None
        print puzzle.save()

    verify_puzzle_progresses(game)
    print "Created %s with id %s" % (game.name, game.id)


def verify_puzzle_progresses(game):
    teams = list(game.teams.all())
    for puzzle in game.puzzles.all():
        for team in teams:
            print PuzzleProgress.objects.get_or_create(
                puzzle=puzzle, team=team)[0]
