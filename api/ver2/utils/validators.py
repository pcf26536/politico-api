"""from flask_jwt_extended import (get_jwt_identity)
from api.ver1.utils import error
from api.ver2.utils.strings import status_401, admin_key
from api.ver2.models.users import User
from api.strings import id_key"""
import datetime
import re


def is_bool(*args):
    for arg in args:
        if not isinstance(arg, bool):
            return False
    return True


def is_string(*args):
    for arg in args:
        if not isinstance(arg, str):
            return False
    return True


def is_number(*args):
    for arg in args:
        if not isinstance(arg, int) or isinstance(arg, float):
            return False
    return True


def is_int(*args):
    for arg in args:
        if not isinstance(arg, int):
            return False
    return True


"""
def is_not_admin():
    user = User().get_by(id_key, get_jwt_identity())

    if not user[admin_key]:
        return error(
            "Unauthorized: This action is reserved to Admins only", status_401)
    return None
"""

def is_valid_email(email):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return False
    return True


def has_min_pass_length(value):
    if len(value) < 6:
        return False
    return True


def has_min_name_length(name):
    if len(name) < 3:
        return False
    return True


def valid_date(date):
    try:
        datetime.datetime.strptime(date, "%d/%m/%y")
        return True
    except ValueError:
        return False


def no_date_diff(date):
    d = datetime.datetime.strptime(date, "%d/%m/%y")
    diff = datetime.datetime.now() - d
    if diff.days:
        return False
    return True

