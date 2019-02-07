from api.ver1.parties.strings import party_key
from api.ver1.utils import name_error_resp
from api.strings import ok_str
import re

def validate_hqAdd(value):
    pass

def validate_logoUrl(value):
    pass

def validate_partyName(name):
    if not (re.match(r'[a-zA-Z]{1,}', name) and not(re.search(r"\s{2,}", name)) and (len(name) > 2)):
        return name_error_resp(party_key, name)
    return ok_str
