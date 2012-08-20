from .models import Membership

def check_staff(user, game):
    try:
        membership = Membership.objects.get(player__user=user, game=game)
    except Membership.DoesNotExist:
        return False
    if not membership.team:
        return False
    else:
        if membership.team.staff:
            return True
        else:
            return False
    return False