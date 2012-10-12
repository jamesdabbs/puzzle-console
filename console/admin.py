from django.contrib import admin

from .models import Game, Team, Player, Membership, Puzzle, UniqueRandom, \
                    PuzzleProgress


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end')
admin.site.register(Game, GameAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('game', 'number', 'staff', 'captain', 'competitive', 'points')
    list_filter = ('game',)
admin.site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    def email(self, player):
        return player.user.email

    list_display = ('name', 'email', 'description')
admin.site.register(Player, PlayerAdmin)


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('game', 'player', 'team')
    list_filter = ('game',)
admin.site.register(Membership, MembershipAdmin)


class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('game', 'number', 'title', 'code', 'open', 'close')
    list_filter = ('game',)
admin.site.register(Puzzle, PuzzleAdmin)


class PuzzleProgressAdmin(admin.ModelAdmin):
    list_display = ('team', 'puzzle', 'status', 'time_opened', 'time_solved',
                    'time_remaining', 'points')
    list_filter = ('puzzle__game', 'team')
admin.site.register(PuzzleProgress, PuzzleProgressAdmin)


class UniqueRandomAdmin(admin.ModelAdmin):
    def game(self, code):
        return code.puzzle.game

    list_display = ('code', 'puzzle', 'game')
    list_filter = ('puzzle__game',)
admin.site.register(UniqueRandom, UniqueRandomAdmin)
