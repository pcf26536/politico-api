from api.strings import id_key
from api.ver1.users.strings import *
from api.ver1.users.models import users
from api.ver2.utils.strings import correct_pass, short_pass, password_key


user_with_correct_signup_data = users[0]
user_with_correct_signup_data[password_key] = correct_pass
del user_with_correct_signup_data[admin]
del user_with_correct_signup_data[id_key]

user_with_correct_signup_data_2 = users[1]
user_with_correct_signup_data_2[password_key] = correct_pass
del user_with_correct_signup_data_2[admin]
del user_with_correct_signup_data_2[id_key]

user_with_missing_signup_data = user_with_correct_signup_data.copy()
del user_with_missing_signup_data[fname]

user_with_wrong_name_format = user_with_correct_signup_data.copy()
user_with_wrong_name_format[lname] = '@@@##'

user_with_wrong_mail_format = user_with_correct_signup_data.copy()
user_with_wrong_mail_format[email] = '3##%##dfdfefdfd.cdfdf'

user_with_wrong_pass_length = user_with_correct_signup_data.copy()
user_with_wrong_pass_length[password_key] = short_pass


user_with_wrong_passport_url = user_with_correct_signup_data.copy()
user_with_wrong_passport_url[pspt] = 'fgrgfgfgf'

user_with_wrong_phone_format = user_with_correct_signup_data.copy()
user_with_wrong_phone_format[phone] = '07adsdvddf'

