from api.ver1.utils import error, success, status_201, provide_field_value
from api.strings import ok_str, name_key, status_400, type_key
from api.ver1.parties.strings import hqAddKey, logoUrlKey, party_key
from api.ver1.offices.strings import office_key
from api.ver1.parties.validators import validate_partyname, validate_logourl, validate_hqadd
from api.ver1.offices.validators import validate_officeName, validate_officeType


def validate_dict(data_dict, entity):
        """This function validates a dictionary def and rejects or accepts it"""
        fields = []
        for key, value in data_dict.items():
            if not value:
                fields.append(key)
                continue
            if len(fields) > 0:
                return provide_field_value(entity, fields)
            elif key == hqAddKey:
                status = validate_hqadd(value)
                if not status == ok_str:
                    return status
            elif key == logoUrlKey:
                status = validate_logourl(value)
                if not status == ok_str:
                    return status
            elif key == type_key:
                status = validate_officeType(value)
                if not status == ok_str:
                    return status
            elif key == name_key:
                status = None
                if entity == party_key:
                    status = validate_partyname(value)
                elif entity == office_key:
                    status = validate_officeName(value)
                if not status == ok_str:
                    return status
        if fields:
            return provide_field_value(entity, fields)
        return ok_str


def validate_id(entity, entity_id):
    try:
        int(entity_id)
        return ok_str
    except Exception:
        return error("The {} id [{}] is not of correct format".format(entity, entity_id), status_400)


def add_entity_check(entity, data_dict, data_list):
    status = validate_dict(data_dict, entity)
    if status == ok_str:
        data_list.append(data_dict)
        return success(code=status_201, data=[data_dict]) # return list of parties to display added party
    return status
