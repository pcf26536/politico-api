from .skeleton import Skeleton
from api.ver2.utils.validators import is_bool, is_string, is_valid_email, has_min_pass_length, invalid_name
from api.ver1.users.strings import *
from api.ver1.parties.strings import imageTypes
from api.strings import id_key, status_400
import re


class User(Skeleton):
    def __init__(
            self, Id=None, fname=None, lname=None, email=None, phone=None,
            passport_url=None, password=None, is_admin=False, table='politico_users'):
        super().__init__('User', table)
        self.Id = Id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone
        self.passport_url = passport_url
        self.password = password
        self.is_admin = is_admin

    def create(self):
        data = super().add(
            id_key + ', ' + 'fname' + ', ' + 'lname' + ', ' + 'phone',
            self.Id, self.fname, self.lname, self.phone
        )
        return data

    def to_json(self):
        # get the object as a json
        return {
            id_key: self.Id,
            fname: self.fname,
            lname: self.lname,
            email: self.email,
            phone: self.phone,
            pspt: self.passport_url,
            admin: self.is_admin
        }

    def from_json(self, json):
        self.__init__(
            json[fname], json[fname], json[email], json[phone],
            json[pspt], json[admin])
        self.Id = json[id_key]
        return self

    def validate_user(self):
        if invalid_name(self.fname, fname):
            self.message = invalid_name(self.fname, fname)['message']
            self.code = invalid_name(self.fname, fname)['code']
            return False

        if invalid_name(self.lname, lname):
            self.message = invalid_name(self.lname, lname)['message']
            self.code = invalid_name(self.lname, lname)['code']
            return False

        if not is_string(self.fname, self.lname):
            self.message = "Integer types are not allowed for a name"
            self.code = status_400
            return False

        if not is_valid_email(self.email):
            self.message = "Invalid email"
            self.code = status_400
            return False

        if not has_min_pass_length(self.password):
            self.message = "Password must be at least 6 characters long"
            self.code = status_400
            return False

        if not is_bool(self.is_admin):
            self.message = "isAdmin is supposed to be a boolean value"
            self.code = status_400
            return False

        if not re.match(r'^07[0-9]{8}$', self.phone):
            self.message = "Enter a valid phone number"
            self.code = status_400
            return False

        if not re.match(r'^[^.]*.[^.]*$', self.passport_url):
            self.message = 'Bad {} format [{}], only one dot(.) should be present.'.format(pspt, self.passport_url)
            self.code = status_400
            return False
        else:
            try:
                name, ext = self.passport_url.split('.')
                if ext not in imageTypes:
                    self.message = 'Only {} image types allowed for {}'.format(imageTypes, pspt)
                    self.code = status_400
                    return False
                elif not re.match(r'[\w.-]{1,256}', name):
                    self.message = 'Bad {} format [{}]. No spaces allowed.'.format(pspt, name)
                    self.code = status_400
                    return False
            except Exception:
                self.message = 'Bad {} format [{}] has no file extension.'.format(pspt, self.passport_url)
                self.code = status_400
                return False

        return super().validate_self()
