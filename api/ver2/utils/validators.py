from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.ver1.utils import error
from api.ver2.utils.strings import status_401, admin_key


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


def is_not_admin():
    user = Users().find_by('id', get_jwt_identity())

    if not user[admin_key]:
        return error(
            "Forbidden: This action is reserved to Admins only", status_401)
    return None
