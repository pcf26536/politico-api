from .strings import office_type_list, office_key
from api.strings import ok_str
from api.ver1.utils import error, name_error_resp
import re

def validate_officeType(value):
    if value in office_type_list:
        return ok_str
    else:
        return error('Incorrect value, office types should be {}'.format(office_type_list), 400)

def validate_officeName(name):
    if not (re.match(r'[a-zA-Z]{3,}', name) and not(re.search(r"\s{2,}", name))):
        return name_error_resp(office_key, name)
    return ok_str