from api.ver1.parties.strings import party_key
from api.ver1.utils import name_error_resp, error
from api.strings import ok_str
from .strings import logoTypes
import re

def validate_hqAdd(value):
    if not re.match(r'^[0-9]+-[0-9]+,\s[A-Za-z]{3,}$', value):
        return error('Bad address format [{}], expected format > [Address-Code, Town] e.g [20100-0100, Nairobi].'.format(value), 400)
    return ok_str

def validate_logoUrl(value):
    if not re.match(r'^[^.]*.[^.]*$', value):
        return error('Bad filename format [{}], only one dot(.) should be present.'.format(value), 400)
    else:
        try:
            name, ext = value.split('.')
            if not ext in logoTypes:
                return error('Only {} image types allowed'.format(logoTypes), 405)
            elif not re.match(r'[\w.-]{1,256}', name):
                return error('Bad filename format [{}]. No spaces allowed.'.format(name), 400)
            else:
                return ok_str
        except Exception:
            return error('Bad filename format [{}] has no file extension.'.format(value), 400)

def validate_partyName(name):
    if not (re.match(r'[a-zA-Z]{1,}', name) and not(re.search(r"\s{2,}", name)) and (len(name) > 2)):
        return name_error_resp(party_key, name)
    return ok_str
