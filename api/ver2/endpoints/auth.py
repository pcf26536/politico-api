from flask import request, Blueprint
from werkzeug.security import check_password_hash
from api.strings import post_method, status_201, id_key, status_404, status_200, status_400
from api.ver1.utils import error, no_entry_resp, check_form_data, field_missing_resp, success
from api.ver1.users.strings import *
from api.ver2.utils.strings import password_1, password_2, admin_key, user_entity, token_key, user_key, password_key
from api.ver2.models.users import User
from api.ver2.models.auth import Auth
from api.ver2.utils.validators import is_valid_email

auth = Blueprint('auth', __name__)


@auth.route('/auth/signup', methods=[post_method])
def signup():
    fields = [fname, lname, email, pspt, phone, password_1, password_2]
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
            )
            if not user.validate_user():
                return error(user.message, user.code)
            user_auth = Auth(email=res_data[email], password=res_data[password_1])
            if not user_auth.validate_auth():
                return error(user_auth.message, user_auth.code)
            user_auth.create()
            user.create()
            return success(status_201, [{
                token_key: user_auth.access_token,
                user_key: {user.to_json()}
            }])
        except Exception as e:
            return field_missing_resp(user_entity, fields, e.args[0])
    else:
        return no_entry_resp(user_entity, fields)


@auth.route('/auth/login', methods=[post_method])
def login():
    fields = [email, password_key]
    res_data = check_form_data(user_key, request, fields)
    if res_data:
        try:
            code = None
            message = ''
            mail = res_data[email]
            password = res_data[password_key]
            login_user = Auth().get_by(email, mail)
            if not login_user:
                code = status_404
                message = "user does not exits in the database"
            elif not check_password_hash(login_user.to_json()[password_key], password):
                code = status_400
                message = 'Incorrect password provided'
            else:
                user = Auth(Id=login_user.to_json()[id_key])
                user.create_auth_tokens()
                code = status_200
                data = {
                    token_key: user.access_token,
                    user_key: user
                }
                return success(code, [data])
            return error(message, code)
        except Exception as e:
            return field_missing_resp(user_entity, fields, e.args[0])
    else:
        return no_entry_resp(user_entity, fields)


@auth.route('/auth/reset', methods=[post_method])
def reset():
    message = ''
    code = status_400
    fields = [email]
    data = check_form_data(user_key, request, fields)
    if data:
        try:
            mail = data[email]
            if is_valid_email(mail):
                if User().get_by(email, mail):
                    res_data = [{
                        'message': 'Check your email for password reset link',
                        'email': mail
                    }]
                    code = status_200
                    return success(code, res_data)
                else:
                    message = 'No user is registered with that email'
                    code = status_404
            else:
                message = 'Please enter a valid email'
        except Exception as e:
            message = 'Please provide an email to reset you password'
    else:
        message = 'No Input Received: Please input an email to reset you password'
    return error(message, code)
