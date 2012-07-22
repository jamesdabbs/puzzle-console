from django.db.utils import IntegrityError

class TeamBuildingException(IntegrityError):
    pass