from .strings import office_type_list, office_key
from api.strings import ok_str
from api.ver1.utils import error, name_error_resp
from .models import political_offices
from api.ver1.utils import exists, exists_resp
import re

def validate_officeType(value):
    if not re.match(r"^\s{1,}$", value):
        if value in office_type_list:
            return ok_str
        else:
            return error('Incorrect value [{}], office types should be {}'.format(value, office_type_list), 400)
    else:
        return error("Please provide ['type'] value(s) for the office", 400)

def validate_officeName(name):
    if not (re.match(r'[a-zA-Z]{3,}', name) and not(re.search(r"\s{2,}", name))):
        return name_error_resp(office_key, name)
    elif not exists(name, political_offices, name_key) == not_found:
        return exists_resp(office_key, name, name_key)
    return ok_str