from .models import political_offices
from api.strings import *
from api.ver1.utils import generate_id, error, success
from .strings import *


class Office:
    def __init__(self, id=None, type=None, name=None):
        self.id = id
        self.type = type
        self.name = name

    def exists(self, id):
        for office in political_offices:
            if office[id_key] == self.id:
                return office
        return error(office_id_str + not_found, status_404)

    def validate_name(self, name):
        if len(name) < 3:
            return error(message="The office name provided is too short", code=status_400)
        return 'OK'
    
    def validate_office(self, office):
        """This function validates a office and rejects or accepts it"""
        for key, value in office.items():
            if not value:
                return error(message="Please provide a {} for the office".format(key), code=status_400)
            elif key == name_key:
                status = self.validate_name(value)
                if not status == 'OK':
                    return status
        return 'OK'

    #create a political office.
    def add_office(self):
        """"Add a political office passed on instantiation, generates auto id"""
        office = { 
                    id_key: generate_id(political_offices), 
                    name_key:self.name, 
                    type_key: self.type
                }
        status = self.validate_office(office)
        if status == 'OK':
            political_offices.append(office)
            return success(code=status_201, data=[office]) # return list of offices to display added office
        return status
        
    #gets a specific office.
    def get_office(self):
        status = self.exists(self.id)
        if type(status) == dict:
            return success(status_201, [status])
        return status

     #gets all offices.
    def get_offices(self):
        return success(status_201, political_offices)