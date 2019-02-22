from flask import make_response, jsonify
from api.ver1.parties.strings import imageTypes
from api.strings import *
import re


def generate_id(list):
    """ Creates a unique ID for a new item to be added to the list"""
    return len(list) + 1


def success(code, data=None):
    """ Creates a success basic response """
    resp = {
        status_key: code,
        data_key: data
    }
    return make_response(jsonify(resp), code)


def error(message, code):
    """ Creates an error basic response """
    resp = {
        status_key: code,
        error_key: message
    }
    return make_response(jsonify(resp), code)


def exists(value, item_list, key):
    """Check if item exits in dict list via id and returns item or not found"""
    for item in item_list:
        if item[key] == value:
            return item
    return not_found


def check_form_data(entity, request, fields):
    data = request.get_json()
    form_data = request.form # check for any form data
    if not data or not len(data):
        if form_data:
            return form_data
        else:
            return None
    return data


def name_length_resp(entity, name):
    return error(
        message="The {} name [{}] provided is too short".format(entity, name),
        code=400)


def check_name_base(entity, name, data_list):
    if not (re.match(r'[a-zA-Z]{3,}', name)
            and not(re.search(r"\s{2,}", name))):
        return name_format_resp(entity, name)
    elif not (len(name) > 2):
        return name_length_resp(entity, name)
    elif not exists(name, data_list, name_key) == not_found:
        return exists_resp(entity, name, name_key)
    return ok_str


def invalid_name(entity, name):
    if not (re.match(r'[a-zA-Z]{3,}', name)
            and not(re.search(r"\s{2,}", name))):
        return name_format_resp(entity, name)
    elif not (len(name) > 2):
        return name_length_resp(entity, name)
    return None


def provide_field_value(entity, fields):
    return error(
        message="Please provide {} value(s) for the {}".format(fields, entity),
        code=status_400)


def not_found_resp(entity):
    return error(entity + ' ' + not_found, status_404)


def no_entry_resp(entity, fields):
    return error(
        "No data was provided, fields {} required to create {}"
        "".format(fields, entity),
        status_400)


def field_missing_resp(entity, fields, field, action=None):
    if action:
        return error(
            "{} field is required to {}".format(field, action),
            status_400)
    return error(
        "{} field is required to create {}".format(field, entity),
        status_400)


def method_not_allowed(method):
    return error(
        "method [{}] not allowed on this endpoint".format(method),
        status_405)


def runtime_error_resp(e):
    return error('Runtime Exception: {}'.format(str(e)), 500)


def name_format_resp(entity, name):
    return error(
        message="The {} name [{}] provided is invalid/wrong format"
                "".format(entity, name),
        code=status_400)


def exists_resp(entity, value, field):
    return error(
        'Conflict: {} with {} as {} already exists'
        ''.format(entity, value, field), status_400)


def validate_image(entity, value):
    if not re.match(r'^[^.]*.[^.]*$', value):
        return error(
            'Bad {} format [{}], only one dot(.) should be present.'
            ''.format(entity, value), status_400)
    else:
        try:
            name, ext = value.split('.')
            if ext not in imageTypes:
                return error(
                    'Only {} image types allowed'
                    ''.format(imageTypes), 405)
            elif not re.match(r'[\w.-]{1,256}', name):
                return error(
                    'Bad {} format [{}]. No spaces allowed.'
                    ''.format(entity, name), status_400)
            else:
                return None
        except Exception:
            return error(
                'Bad {} format [{}] has no file extension.'
                ''.format(entity, value), 400)
