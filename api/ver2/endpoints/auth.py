from flask import request, Blueprint
from werkzeug.security import check_password_hash
from api.strings import post_method, status_201, id_key, status_404, status_200, status_400
from api.ver1.utils import error, no_entry_resp, check_form_data, field_missing_resp, success
from api.ver1.users.strings import *
from api.ver2.utils.strings import password_1, password_2, admin_key, user_entity, token_key, user_key, password_key
from api.ver2.models.users import User
from api.ver2.models.auth import Auth
from api.ver2.utils.validators import is_valid_email, invalid_passwords
from api.ver2.utils.utilities import system_unavailable
from api.ver2.utils import is_not_admin
from werkzeug.security import generate_password_hash
import traceback

auth = Blueprint('auth', __name__)
reset_token = None
reset_user = None


@auth.route('/auth/signup', methods=[post_method])
def signup():
    try:
        fields = [fname, lname, email, pspt, phone, password_key]
        res_data = check_form_data(user_entity, request, fields)
        if res_data:
            try:
                user = User(
                    fname=res_data[fname],
                    lname=res_data[lname],
                    email=res_data[email],
                    passport_url=res_data[pspt],
                    phone=res_data[phone],
                    password=res_data[password_key],
                )
            except Exception as e:
                return field_missing_resp(user_entity, fields, e.args[0])

            if not user.validate_user():
                return error(user.message, user.code)
            user_auth = Auth(email=res_data[email], password=res_data[password_1])
            if not user_auth.validate_auth():
                return error(user_auth.message, user_auth.code)
            user_auth.create()
            user.Id = user_auth.Id
            user.create()
            return success(status_201, [{
                token_key: user_auth.access_token,
                user_key: user.to_json()
            }])

        else:
            return no_entry_resp(user_entity, fields)
    except Exception as e:
        return system_unavailable(e)


@auth.route('/auth/login', methods=[post_method])
def login():
    try:
        fields = [email, password_key]
        res_data = check_form_data(user_key, request, fields)
        if res_data:
            try:
                code = None
                message = ''
                mail = res_data[email]
                password = res_data[password_key]
            except Exception as e:
                return field_missing_resp(user_entity, fields, e.args[0], 'login')
            login_user = Auth().get_by(email, mail)
            if not login_user:
                code = status_404
                message = "user does not exits in the database"
            elif not check_password_hash(login_user[password_key], password):
                code = status_400
                message = 'Incorrect password provided'
            else:
                user = Auth(Id=login_user[id_key], email=mail)
                user.create_auth_tokens()
                if login_user[admin_key]:
                    user_in4 = Auth().get_admin(email, mail)
                else:
                    user_in4 = User().get_by_id(login_user[id_key])
                code = status_200
                data = {
                    token_key: user.access_token,
                    user_key: user_in4
                }
                return success(code, [data])
            return error(message, code)
        else:
            return no_entry_resp(user_entity, fields)
    except Exception as e:
        return system_unavailable(e)


@auth.route('/auth/reset', methods=[post_method])
def reset():
    try:
        message = ''
        code = status_400
        fields = [email]
        data = check_form_data(user_key, request, fields)
        if data:
            try:
                data[email]
            except ValueError:
                message = 'Please provide an email to reset you password'
            try:
                mail = data[email]
                if is_valid_email(mail):
                    user = Auth().get_by(email, mail)
                    if user:
                        global reset_token, reset_user
                        res_user = Auth(Id=user['id'])
                        res_user.create_auth_tokens()
                        reset_token = res_user.access_token
                        reset_user = mail
                        res_data = [{
                            'message': 'Check your email for password reset link',
                            'email': mail
                        }]
                        body = 'Click this link to reset your password:\n'\
                               + request.base_url + '/link/' + reset_token
                        recipients = [mail]
                        code = status_200
                        print(body)
                        return success(code, res_data)
                    else:
                        message = 'No user is registered with that email'
                        code = status_404
                else:
                    message = 'Please enter a valid email'
            except Exception as e:
                return error('runtime exception: {}, {}'.format(e.args[0], traceback.print_exc()), 500)
        else:
            message = 'No Input Received: Please input an email to reset you password'
        return error(message, code)
    except Exception as e:
        return system_unavailable(e)


@auth.route('/auth/reset/link/<string:token>', methods=[post_method])
def reset_link(token):
    try:
        if token == reset_token:
            fields = [password_1, password_2]
            data = check_form_data(user_key, request, fields)
            if data:
                try:
                    pass1 = data[password_1]
                    pass2 = data[password_2]
                    invalid = invalid_passwords(pass1, pass2)
                    if not invalid:
                        user = Auth().patch(password_key, generate_password_hash(pass1), Auth().get_by('email', reset_user)[0]['id'])
                        return success(200, [{'message': 'password reset successful', 'user': user}])
                    return error(invalid['message'], invalid['code'])
                except Exception as e:
                    return error(
                        'Please provide a value for {} to reset you password'.format(e.args[0]),
                        status_400
                    )
            else:
                return error(
                    'Please input New Password twice to reset current password. fields={}'.format(fields),
                    status_400
                )
        return error('Invalid token please try again', status_400)
    except Exception as e:
        return system_unavailable(e)
