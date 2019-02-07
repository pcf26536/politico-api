from api.ver1.utils import generate_id, error, success, exists
from api.strings import ok_str, name_key, status_400, type_key
from api.ver1.parties.strings import hqAddKey, logoUrlKey, party_key
from api.ver1.offices.strings import office_key
import re
from api.ver1.parties.validators import validate_partyName
from api.ver1.offices.validators import validate_officeName, validate_officeType

def validate_name(name, entity):
    if not (re.match(r'[a-zA-Z]{3,}', name) and not(re.search(r"\s{2,}", name)) and (len(name) > 2)):
        return error(message="The {} name {} provided is too short or has a wrong format".format(entity, name), code=status_400)
    return ok_str


def validate_dict(data_dict, entity):
        """This function validates a dictionary def and rejects or accepts it"""
        for key, value in data_dict.items():
            if not value:
                return error(message="Please provide a {} for the {}".format(key, entity), code=status_400)
            elif key == hqAddKey:
                pass
            elif key == logoUrlKey:
                pass
            elif key == type_key:
                pass
            elif key == name_key:
                status = None
                if entity == party_key:
                    status = validate_partyName(value)
                elif entity == office_key:
                    status = validate_officeName(value)
                if not status == ok_str:
                    return status
        return ok_str


def validate_id(entity, entity_id):
    try:
        int(entity_id)
        return ok_str
    except Exception:
        return error("The {} id [{}] is not of correct format".format(entity, entity_id), status_400)
        