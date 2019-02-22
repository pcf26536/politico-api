import datetime
import re
from api.ver2.utils.strings import evidence_types
from api.strings import status_400
from api.ver2.utils.strings import password_1, password_2


def invalid_passwords(pass1, pass2):
    if not len(pass1):
        message = "Please Input a password for {}".format(password_1)
        code = status_400
        return {'message': message, 'code': code}

    if not len(pass2):
        message = "Please Input a password for {}".format(password_2)
        code = status_400
        return {'message': message, 'code': code}

    if not pass1 == pass2:
        message = "Passwords mismatch"
        code = status_400
        return {'message': message, 'code': code}

    if not (has_min_pass_length(pass1) or has_min_pass_length(pass2)):
        message = "Password must be at least 6 characters long"
        code = status_400
        return {'message': message, 'code': code}
    return None


def invalid_evidence(evidence):
    if not re.match(r'^[^.]*.[^.]*$', evidence):
        return ['Bad evidence [{}] file extension.'.format(evidence), status_400]
    else:
        try:
            name, ext = evidence.split('.')
            if ext not in evidence_types:
                return ['Only {} types allowed'.format(evidence_types),
                        status_400]
        except Exception:
            return ['Bad evidence format [{}] has no file extension.'.format(
                evidence), status_400]
    return None


def process_evidence(evidence):
    ev_str = ''
    for e in evidence:
        ev_str = ev_str + ', ' + e
    return ev_str


def invalid_body(body):
    if not len(body) > 11:
        return ['The evidence text is too short', 400]
    elif not re.match(r'^.{12,}$', body):
        return ['Invalid evidence body', 400]
    return None


def is_bool(*args):
    for arg in args:
        if not isinstance(arg, bool):
            return False
    return True


def is_string(*args):
    for arg in args:
        if not isinstance(arg, str):
            return False
    return True


def is_number(*args):
    for arg in args:
        if not isinstance(arg, int) or isinstance(arg, float):
            return False
    return True


def is_int(*args):
    for arg in args:
        try:
            int(arg)
        except Exception:
            return False
    return True


def is_valid_email(email):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return False
    return True


def has_min_pass_length(value):
    if len(value) < 6:
        return False
    return True


def has_min_name_length(name):
    if len(name) < 3:
        return False
    return True


def valid_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def no_date_diff(date):
    d = datetime.datetime.strptime(date, "%Y-%m-%d")
    diff = datetime.datetime.now() - d
    if diff.days:
        return False
    return True


def invalid_name(name, entity):
    if not (re.match(r'[a-zA-Z]{3,}', name)
            and not(re.search(r"\s{2,}", name))):
        return {
            'message': "The {} name [{}] provided is invalid/wrong format"
                       "".format(entity, name), 'code': status_400}
    elif not (len(name) > 2):
        return {
            'message': "The {} name [{}] provided is too short"
                       "".format(entity, name), 'code': status_400}
    return None

