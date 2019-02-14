from flask import Blueprint, request
from api.strings import post_method, status_201
from api.ver1.utils import error, no_entry_resp, check_form_data, field_missing_resp, success
from api.ver1.users.strings import *
from api.ver2.utils.strings import password_1, password_2, admin_key, user_entity, token_key, user_key
from api.ver2.models.users import User

# blueprint for auth
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/signup', methods=[post_method])
def signup():
    fields = [fname, lname, email, pspt, phone, password_1, password_2, admin_key]
    res_data = check_form_data(user_entity, request, fields)
    if res_data:
        try:
            user = User(
                fname=res_data[fname],
                lname=res_data[lname],
                email=res_data[email],
                passport_url=res_data[pspt],
                phone=res_data[phone],
                password1=res_data[password_1],
                password2=res_data[password_2],
                is_admin=res_data[admin_key]
            )
            if not user.validate_user():
                return error(user.message, user.code)
            user.create()
            return success(status_201, [{
                token_key: user.access_token,
                user_key: {user.to_json()}
            }])
        except Exception as e:
            return field_missing_resp(user_entity, fields, e.args[0])
    else:
        return no_entry_resp(user_entity, fields)


