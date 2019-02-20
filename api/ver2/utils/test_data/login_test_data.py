from api.ver1.users.strings import email
from api.ver2.utils.strings import password_key, password_1
from .signup_test_data import user_with_correct_signup_data

user_with_correct_credentials = {
                email: user_with_correct_signup_data[email],
                password_key: user_with_correct_signup_data[password_key]
            }

user_with_incorrect_mail = user_with_correct_credentials.copy()
user_with_incorrect_mail[email] = 'me&you@them'

user_with_incorrect_password = user_with_correct_credentials.copy()
user_with_incorrect_password[password_key] = '@QwertYEv'

user_with_missing_mail = user_with_correct_credentials.copy()
del user_with_missing_mail[email]

user_with_missing_pass = user_with_correct_credentials.copy()
del user_with_missing_pass[password_key]
