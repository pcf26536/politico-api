import jwt
from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required)
from flask_jwt_extended import (get_jwt_identity, get_raw_jwt)
from werkzeug.security import generate_password_hash
import datetime
import re
from .skeleton import Skeleton
from api.ver2.utils.validators import is_number, is_bool, is_not_admin, is_string


class Users(Skeleton):
    pass