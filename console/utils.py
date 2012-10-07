from .models import Membership

def check_staff(user, game):
    try:
        membership = Membership.objects.get(player__user=user, game=game)
        return membership.team && membership.team.staff
    except Membership.DoesNotExist:
        return False