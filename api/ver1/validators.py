from api.ver1.utils import generate_id, error, success, exists
from api.strings import *

def validate_name(name):
    if len(name) < 3:
        return error(message="The party name provided is too short", code=status_400)
    return ok_str


def validate_dict(data_dict):
        """This function validates a dictionary def and rejects or accepts it"""
        for key, value in data_dict.items():
            if not value:
                return error(message="Please provide a {} for the office".format(key), code=status_400)
            elif key == name_key:
                status = validate_name(value)
                if not status == ok_str:
                    return status
        return 'OK'