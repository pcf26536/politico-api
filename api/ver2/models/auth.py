from flask_jwt_extended import (create_access_token, create_refresh_token)
from werkzeug.security import generate_password_hash
from .skeleton import Skeleton
from api.ver2.utils.validators import is_bool, is_string, is_valid_email, has_min_pass_length, invalid_name
from api.ver1.users.strings import *
from api.ver1.parties.strings import imageTypes
from api.strings import id_key, status_409, status_400
from api.ver2.utils.strings import password_key, admin_key
import re


class Auth(Skeleton):
    def __init__(
            self, Id=None, email=None, password=None, is_admin=False, table='politico_auth'):
        super().__init__('User', table)
        self.Id = Id
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def create_auth_tokens(self):
        self.access_token = create_access_token(identity=self.Id)
        self.refresh_token = create_refresh_token(identity=self.Id)

    def create(self):
        data = super().add(
            email + ', ' + password_key + ', ' + admin_key,
            self.email, generate_password_hash(self.password), self.is_admin
        )
        self.Id = data.get(id_key)
        self.create_auth_tokens()
        return data

    def to_json(self):
        # get the object as a json
        return {
            id_key: self.Id,
            email: self.email,
            admin: self.is_admin
        }

    def validate_auth(self):
        if self.get_by(email, self.email):
            self.message = "A {} with that email already exists".format(
                self.entity)
            self.code = status_409
            return False
