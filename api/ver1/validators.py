from api.ver1.utils import generate_id, error, success, exists
from api.strings import ok_str, name_key, status_400

def validate_name(name, entity):
    if len(name) < 3:
        return error(message="The {} name {} provided is too short".format(entity, name), code=status_400)
    return ok_str


def validate_dict(data_dict, entity):
        """This function validates a dictionary def and rejects or accepts it"""
        for key, value in data_dict.items():
            if not value:
                return error(message="Please provide a {} for the {}".format(key, entity), code=status_400)
            elif key == name_key:
                status = validate_name(value, entity)
                if not status == ok_str:
                    return status
        return ok_str


def validate_id(entity, entity_id):
    try:
        int(entity_id)
        return ok_str
    except Exception:
        return error("The {} id [{}] is not of correct format".format(entity, entity_id), status_400)
        