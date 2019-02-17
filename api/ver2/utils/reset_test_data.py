from api.ver1.users.strings import email
from .signup_test_data import user_with_correct_signup_data

user_with_correct_email = {
                email: user_with_correct_signup_data[email]
        }

user_with_unexisting_email = user_with_correct_email.copy()
user_with_unexisting_email[email] = 'meandyou@them.us'

user_with_invalid_email = user_with_correct_email.copy()
user_with_invalid_email[email] = 'dfdfdfeee232ds.org'

user_with_no_email = user_with_correct_email.copy()
del user_with_no_email[email]