from flask_jwt_extended import (get_jwt_identity)
from api.ver1.utils import error
from api.ver2.utils.strings import status_401, admin_key
from api.ver2.models.users import User
from api.strings import id_key


def is_not_admin():
    user = User().get_by(id_key, get_jwt_identity())

    if not user.to_json()[admin_key]:
        return error(
            "Forbidden: This action is reserved to Admins only", status_401)
    return None
