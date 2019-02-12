from api.ver1.parties.strings import party_key
from api.ver1.utils import name_format_resp, name_length_resp, error, exists, exists_resp
from api.strings import ok_str, not_found, name_key
from .strings import logoTypes, hqAddKey
from .models import political_parties
from api.ver1.validators import validate_name_base
import re

def validate_hqAdd(value):
    if not re.match(r'^[0-9]+-[0-9]+,\s[a-zA-Z]{3,}$', value):
        return error('Bad address format [{}], expected format > [Address-Code, Town] e.g [20100-0100, Nairobi].'.format(value), 400)
    elif not exists(value, political_parties, hqAddKey) == not_found:
        return exists_resp(party_key, value, hqAddKey)
    return ok_str

def validate_logoUrl(value):
    if not re.match(r'^[^.]*.[^.]*$', value):
        return error('Bad image logo format [{}], only one dot(.) should be present.'.format(value), 400)
    else:
        try:
            name, ext = value.split('.')
            if not ext in logoTypes:
                return error('Only {} image types allowed'.format(logoTypes), 405)
            elif not re.match(r'[\w.-]{1,256}', name):
                return error('Bad image logo format [{}]. No spaces allowed.'.format(name), 400)
            else:
                return ok_str
        except Exception:
            return error('Bad image logo format [{}] has no file extension.'.format(value), 400)

def validate_partyName(name):
    return validate_name_base(party_key, name, political_parties)
