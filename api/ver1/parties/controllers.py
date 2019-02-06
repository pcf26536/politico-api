from .models import political_parties
from api.strings import *
from api.ver1.utils import generate_id, error, success
from .strings import *

class Party(object):
    """Party model to store party data in data structures"""
    def __init__(self, id=None, name=None, hqAddress=None, logoUrl=None):
        self.id = id
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl

    def validate_name(self, name):
        if len(name) < 3:
            return error(message="The party name provided is too short", code=status_400)
        return 'OK'
    
    def validate_party(self, party):
        """This function validates a party and rejects or accepts it"""
        for key, value in party.items():
            if not value:
                return error(message="Please provide a {} for the party".format(key), code=status_400)
            elif key == name_key:
                status = self.validate_name(value)
                if not status == 'OK':
                    return status
        return 'OK'
    
    def exists(self, id):
        for party in political_parties:
            if party[id_key] == self.id:
                return party
        return error(party_id_str + not_found, status_404)


    #create a political party.
    def add_party(self):
        """"Add a political party passed on instantiation, generates auto id"""
        party = { 
                    id_key: generate_id(political_parties), 
                    name_key:self.name, 
                    hqAddKey: self.hqAddress,
                    logoUrlKey: self.logoUrl 
                }
        status = self.validate_party(party)
        if status == 'OK':
            political_parties.append(party)
            return success(code=status_201, data=[party]) # return list of parties to display added party
        return status

    #deletes a party.
    def delete_party(self):
        for i in range(len(political_parties)):
            if political_parties[i]['id'] == self.id:
                return success(
                    code=status_200, 
                    data=[ { msg_key: '{} deleted successfully'.format(political_parties.pop(i)[name_key]) } ]
                    )
        return error(party_id_str + not_found, status_404)
        
    #gets a specific party.
    def get_party(self):
        status = self.exists(self.id)
        if type(status) == dict:
            return success(status_201, [status])
        return status

    # edits a specific party.
    def edit_party(self):
        status = self.exists(self.id)
        if type(status) == dict:
            state = self.validate_name(self.name)
            if state == 'OK':
                status[name_key] = self.name
                return success(status_200, [status])
            return state
        return status

     #gets all parties.
    def get_parties(self):
        return success(status_201, political_parties)
