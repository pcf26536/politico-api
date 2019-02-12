from .strings import office_type_list, office_key
from api.strings import ok_str, name_key, not_found
from api.ver1.utils import error, name_format_resp, name_length_resp
from .models import political_offices
from api.ver1.utils import exists, exists_resp
from api.ver1.utils import check_name_base
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
    return check_name_base(office_key, name, political_offices)