from api.ver1.utils import error
from flask_jwt_extended import (get_jwt_identity)
from api.ver2.models.auth import Auth


def system_unavailable(e):
    print('Runtime Exception: ' + e.args[0])
    return error(
        message='System unavailable, please try again later!',
        code=500
    )


def get_current_user_id():
    user = Auth().get_by(id_key, get_jwt_identity())
