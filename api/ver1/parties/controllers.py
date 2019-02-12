from .models import political_parties
from api.strings import id_key, name_key, ok_str, status_201, status_200, msg_key, not_found
from api.ver1.utils import generate_id, error, success
from .strings import party_id_str, hqAddKey, logoUrlKey, party_key
from api.ver1.validators import validate_dict, add_entity_check
from api.ver1.utils import exists, not_found_resp
from .validators import validate_partyName

class PartyCont:
    """Party model to store party data in data structures"""
    def __init__(self, Id=None, name=None, hqAddress=None, logoUrl=None):
        self.Id = Id
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl

    #create a political party.
    def add_party(self):
        """"Add a political party passed on instantiation, generates auto id"""
        party = { id_key: generate_id(political_parties), name_key:self.name, hqAddKey: self.hqAddress, logoUrlKey: self.logoUrl }
        return add_entity_check(party_key, party, political_parties)

    #deletes a party.
    def delete_party(self):
        for i in range(len(political_parties)):
            if political_parties[i][id_key] == self.Id:
                return success( code=status_200, data=[{ msg_key: '{} deleted successfully'.format(political_parties.pop(i)[name_key])}])
        return not_found_resp(party_id_str)
        
    #gets a specific party.
    def get_party(self):
        status = exists(self.Id, political_parties, id_key)
        if type(status) == dict:
            return success(status_201, [status])
        return not_found_resp(party_id_str)

    # edits a specific party.
    def edit_party(self):
        status = exists(self.Id, political_parties, id_key)
        if isinstance(status, dict):
            state = validate_partyName(self.name)
            if state == ok_str:
                status[name_key] = self.name
                return success(status_200, [status])
            return state
        return not_found_resp(party_id_str)

     #gets all parties.
    def get_parties(self):
        return success(status_201, political_parties)
