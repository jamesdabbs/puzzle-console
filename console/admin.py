from django.contrib import admin

from .models import Achievement, Clue, Game, Team, Player, Membership, Puzzle,\
                    UniqueRandom, PuzzleProgress, Video


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'team')
    list_filter = ('team__game',)
admin.site.register(Achievement, AchievementAdmin)


class ClueAdmin(admin.ModelAdmin):
    list_display = ('puzzle', 'puzzle_number', 'puzzle_game', 'show_at')
    list_filter = ('puzzle__game',)
    def puzzle_number(self, obj):
        return obj.puzzle.number
    def puzzle_game(self, obj):
        return obj.puzzle.game
admin.site.register(Clue, ClueAdmin)


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end')
admin.site.register(Game, GameAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('game', 'number', 'name', 'staff', 'captain', 'competitive', 'points')
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
    list_display = ('game', 'number', 'title', 'code', 'open', 'close',
            'solution_location')
    list_filter = ('game',)
admin.site.register(Puzzle, PuzzleAdmin)


class PuzzleProgressAdmin(admin.ModelAdmin):
    list_display = ('team', 'puzzle', 'status', 'time_opened', 'time_solved',
                    'time_remaining')
    list_filter = ('puzzle__game', 'team')
admin.site.register(PuzzleProgress, PuzzleProgressAdmin)


class UniqueRandomAdmin(admin.ModelAdmin):
    def game(self, code):
        return code.puzzle.game

    list_display = ('code', 'puzzle', 'game')
    list_filter = ('puzzle__game',)
admin.site.register(UniqueRandom, UniqueRandomAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('game', 'number', 'url', 'open')
    list_filter = ('game',)
admin.site.register(Video, VideoAdmin)
