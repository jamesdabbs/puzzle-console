from django.contrib import admin

from .models import Game, Team, Player, Membership, Puzzle, UniqueRandom


class GameAdmin(admin.ModelAdmin):
    pass
admin.site.register(Game, GameAdmin)


class TeamAdmin(admin.ModelAdmin):
    pass
admin.site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Player, PlayerAdmin)


class MembershipAdmin(admin.ModelAdmin):
    pass
admin.site.register(Membership, MembershipAdmin)


class PuzzleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Puzzle, PuzzleAdmin)


class UniqueRandomAdmin(admin.ModelAdmin):
    pass
admin.site.register(UniqueRandom, UniqueRandomAdmin)