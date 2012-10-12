import csv
import os

from console.models import Game, Player, Team, PuzzleProgress


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


def verify_puzzle_progresses(game):
    teams = list(game.teams.all())
    for puzzle in game.puzzles.all():
        for team in teams:
            print PuzzleProgress.objects.get_or_create(
                puzzle=puzzle, team=team)[0]
