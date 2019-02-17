from flask_jwt_extended import (get_jwt_identity)
from api.ver1.utils import error
from api.ver2.utils.strings import status_401, admin_key
from api.ver2.models.auth import Auth
from api.strings import id_key


def is_not_admin():
    user = Auth().get_by(id_key, get_jwt_identity())

    if not user[admin_key]:
        return error(
            "Forbidden: This action is reserved to Admins only", status_401)
    return None
