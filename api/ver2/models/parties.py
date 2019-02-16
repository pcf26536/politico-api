from .skeleton import Skeleton
from api.strings import id_key, name_key, ok_str, status_key, error_key, status_400
from api.ver1.parties.strings import hqAddKey, logoUrlKey
from api.ver1.parties.validators import validate_hqadd, validate_logourl
from api.ver2.utils.validators import is_string
from api.ver1.utils import invalid_name


class Party(Skeleton):
    def __init__(self, Id=None, name=None, hqAddress=None, logoUrl=None):
        super().__init__('Party', 'politico_parties')

        self.Id = Id
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl

    def to_json(self):
        return {
            id_key: self.Id,
            name_key: self.name,
            hqAddKey: self.hqAddress,
            logoUrlKey: self.logoUrl,
        }

    def create(self):
        data = super().add(
            name_key + ',' + 'hq_address' + ',' +  'logo_url',
            self.name, self.hqAddress, self.logoUrl)

        self.Id = data.get(id_key)
        return data

    def from_json(self, json):
        self.__init__(
            json[name_key],
            json[hqAddKey],
            json[logoUrlKey]
        )
        self.Id = json[id_key]
        return self

    def update(self, new_name):
        self.name = new_name
        return super().patch(name_key, new_name, self.Id)

    def validate_party(self):
        if not is_string(self.name):
            self.message = "Integer types are not allowed for a name field"
            self.code = status_400
            return False

        invalid = invalid_name('party', self.name)
        if invalid:
            self.message = invalid.get_json()[error_key]
            self.code = invalid.get_json()[status_key]
            return False

        logo_valid = validate_logourl(self.logoUrl)
        if not logo_valid == ok_str:
            self.message = logo_valid.get_json()[error_key]
            self.code = logo_valid.get_json()[status_key]
            return False

        add_valid = validate_hqadd(self.hqAddress)
        if not add_valid == ok_str:
            self.message = add_valid.get_json()[error_key]
            self.code = add_valid.get_json()[status_key]
            return False

        if self.get_by('name', self.name):
            self.message = "Conflict: Party with {} as name already exists".format(self.name)
            self.code = 409
            return False

        if self.get_by('hq_address', self.hqAddress):
            self.message = "Conflict: party with {} as hqAddress already exists".format(self.hqAddress)
            self.code = 409
            return False

        return super().validate_self()
