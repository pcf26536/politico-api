from .skeleton import Skeleton
from api.strings import id_key, name_key, type_key, status_201, ok_str, error_key, status_key
from api.ver1.offices.validators import validate_officeName, validate_officeType


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
        valid_type = validate_officeType(self.type)
        if valid_type == ok_str:
            self.message = valid_type[error_key]
            self.code = valid_type[status_key]
            return True

        valid_name = validate_officeName(self.name)
        if valid_name == ok_str:
            self.message = valid_name[error_key]
            self.code = valid_name[status_key]
            return True

        return super().validate_self()
