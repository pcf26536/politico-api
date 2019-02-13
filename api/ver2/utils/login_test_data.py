from api.ver1.users.strings import email
from api.ver2.utils.strings import password_key

user_with_correct_credentials = {
    email : 'muffwaindan@gmail.com',
    password_key : '@QwertY1212'
}

user_with_incorrect_credentials = user_with_correct_credentials
user_with_incorrect_credentials[password_key] = '@QwertYEv'

user_with_missing_credentials = user_with_correct_credentials
user_with_missing_credentials[email] = ''
