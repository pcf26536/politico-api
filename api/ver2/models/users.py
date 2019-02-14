from flask_jwt_extended import (create_access_token, create_refresh_token)
from werkzeug.security import generate_password_hash
from .skeleton import Skeleton
from api.ver2.utils.validators import is_bool, is_string, is_valid_email, has_min_length
from api.ver1.users.strings import *
from api.strings import id_key, status_409
from api.ver2.utils.strings import password_key, user_id_key, status_422


class Users(Skeleton):
    def __init__(
            self, id=None, fname=None, lname=None, email=None, phone=None,
            passport_url=None, password1=None, password2=None, is_admin=False):
        super().__init__('User', 'politico_users')
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone
        self.passport_url = passport_url
        self.password1 = password1
        self.password2 = password2
        self.is_admin = is_admin

    def create_auth_tokens(self):
        self.access_token = create_access_token(identity=self.id)
        self.refresh_token = create_refresh_token(identity=self.id)

    def add(self, *args):
        data = super().add(
            email + ', ' + password_key + ', ' + admin,
            self.email, generate_password_hash(self.password1), self.is_admin
        )
        self.id = data.get(id_key)
        super().add(
            user_id_key + ', ' + fname + ', ' + lname + ', ' + phone,
            self.id, self.fname, self.lname, self.phone
        )
        self.create_auth_tokens()
        return data

    def to_json(self):
        # get the object as a json
        return {
            id_key: self.id,
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
        self.id = json[id_key]
        return self

    def validate_object(self):
        if not is_string(self.fname, self.lname):
            self.message = "Integer types are not allowed for a name"
            self.code = status_422
            return False

        if self.get_by(email, self.email):
            self.message = "A {} with that email already exists".format(
                self.entity)
            self.code = status_409
            return False

        if not is_valid_email(self.email):
            self.message = "Invalid email"
            self.code = status_422
            return False

        if not self.password1 == self.password2:
            self.message = "Passwords mismatch"
            self.code = status_422
            return False

        if not (has_min_length(self.password1) or has_min_length(self.password2)):
            self.message = "Password must be at least 6 characters long"
            self.code = status_422
            return False

        if not is_bool(self.is_admin):
            self.message = "isAdmin is supposed to be a boolean value"
            self.code = status_422
            return False

        return super().validate_self()
