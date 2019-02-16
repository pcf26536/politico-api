from .skeleton import Skeleton
from api.strings import id_key, name_key, type_key, ok_str, error_key, status_key, status_400
from api.ver1.offices.validators import validate_officeName, validate_officeType
from api.ver2.utils.validators import is_string
from api.ver1.utils import invalid_name


class Office(Skeleton):
    def __init__(self, Id=None, office_type=None, name=None):
        super().__init__('Office', 'politico_offices')
        self.Id = Id
        self.type = office_type
        self.name = name

    def create(self):
        data = super().add(name_key + ', ' + type_key, self.name, self.type)
        self.Id = data.get(id_key)
        return data

    def to_json(self):
        return {
            id_key: self.Id,
            name_key: self.name,
            type_key: self.type
        }

    def from_json(self, json):
        self.__init__(json[name_key], json[type_key])
        self.Id = json[id_key]
        return self

    def validate_office(self):
        if not is_string(self.name):
            self.message = "Integer types are not allowed for a name field"
            self.code = status_400
            return False

        if not is_string(self.type):
            self.message = "Integer types are not allowed for type field"
            self.code = status_400
            return False

        valid_type = validate_officeType(self.type)
        if not valid_type == ok_str:
            self.message = valid_type.get_json()[error_key]
            self.code = valid_type.get_json()[status_key]
            return False

        invalid = invalid_name('office', self.name)
        if invalid:
            self.message = invalid.get_json()[error_key]
            self.code = invalid.get_json()[status_key]
            return False

        if self.get_by('name', self.name):
            self.message = "Conflict: office with Women Representative as name already exists"
            self.code = 409
            return True

        return super().validate_self()
