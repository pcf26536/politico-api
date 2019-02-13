from api.ver1.users.strings import email
from api.ver2.utils.strings import password_key

user_with_correct_email = {
    email : 'muffwaindan@gmail.com'
}

user_with_unexisting_email = user_with_correct_email
user_with_unexisting_email[email] = 'meandyou@them.us'

user_with_invalid_email = user_with_correct_email
user_with_invalid_email[email] = 'dfdfdfeee232ds.org'
