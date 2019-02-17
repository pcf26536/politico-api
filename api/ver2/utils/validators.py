import datetime
import re
from api.ver2.utils.strings import evidence_types


def invalid_evidence(value):
    for evidence in value:
        if not re.match(r'^[^.]*.[^.]*$', evidence):
            return ['Bad evidence [{}] file extension.'.format(evidence), 400]
        else:
            try:
                name, ext = evidence.split('.')
                print(name, ext)
                if not ext in evidence_types:
                    return ['Only {} types allowed'.format(evidence_types), 400]
            except Exception:
                return ['Bad evidence format [{}] has no file extension.'.format(evidence), 400]
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
        except:
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
        datetime.datetime.strptime(date, "%y-%m-%d")
        return True
    except ValueError:
        return False


def no_date_diff(date):
    d = datetime.datetime.strptime(date, "%y-%m-%d")
    diff = datetime.datetime.now() - d
    if diff.days:
        return False
    return True


def invalid_name(name, entity):
    if not (re.match(r'[a-zA-Z]{3,}', name) and not(re.search(r"\s{2,}", name))):
        return {'message': "The {} [{}] provided is invalid/wrong format".format(entity, name), 'code': 400}
    elif not (len(name) > 2):
        return {'message' : "The {} [{}] provided is too short".format(entity, name), 'code': 400}
    return None

