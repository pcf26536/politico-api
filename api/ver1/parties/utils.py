from api.ver1.utils import success, error
from api.strings import name_key

def validate_party(party):
    """This function validates a party and rejects or accepts it"""
    for key, value in party.items():
        if not value:
            return error("Please provide a {} for the party".format(key), 400)
        if key == name_key:
            if len(value) < 3:
                return error("The party name provided is too short", 400)