from api.strings import id_key, name_key, type_key, status_201, ok_str
from api.ver1.utils import generate_id, success, exists, not_found_resp
from api.ver1.offices.strings import office_id_str, office_key
from api.ver1.validators import validate_dict, add_entity_check
from api.ver1.offices.models import political_offices


class OfficeCont:
    def __init__(self, Id=None, office_type=None, name=None):
        self.Id = Id
        self.type = office_type
        self.name = name

    # create a political office
    def add_office(self):
        """"Add a political office passed on instantiation, generates auto id"""
        office = { id_key: generate_id(political_offices), name_key: self.name, type_key: self.type }
        return add_entity_check(office_key, office, political_offices)
        
    # gets a specific office.
    def get_office(self):
        """" fetch a specific office via specified id """
        status = exists(self.Id, political_offices, id_key)
        if isinstance(status, dict):
            return success(status_201, [status])
        return not_found_resp(office_id_str)

    # gets all offices.
    def get_offices(self):
        """" fetch all political offices """
        return success(status_201, political_offices)