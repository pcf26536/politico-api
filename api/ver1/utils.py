from flask import make_response, jsonify
from api.strings import *
import re

def generate_id(list):
    """ Creates a unique ID for a new item to be added to the list"""
    return len(list) + 1


def success(code, data=None):
    """ Creates a success basic reponse """
    resp = {
        status_key: code,
        data_key: data
    }
    return make_response(jsonify(resp), code)


def error(message, code):
    """ Creates an error basic reponse """
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
            data = form_data
        else:
            return no_entry_resp(entity, fields)
    return data


def check_name_base(entity, name, data_list):
    if not (re.match(r'[a-zA-Z]{3,}', name) and not(re.search(r"\s{2,}", name))):
        return name_format_resp(entity, name)
    elif not (len(name) > 2):
        return name_length_resp(entity, name)
    elif not exists(name, data_list, name_key) == not_found:
        return exists_resp(entity, name, name_key)
    return ok_str


def not_found_resp(entity):
    return error(entity + not_found, status_404)

def no_entry_resp(entity, fields):
    return error("No data was provided, fields {} required to create {}".format(fields, entity), status_400)

def field_missing_resp(entity, fields, field):
    return error("{} field is required. NOTE: required fields {} to create {}".format(field, fields, entity), status_400)

def method_not_allowed(method):
    return error("method [{}] not allowed on this endpoint".format(method), status_405)

def runtime_error_resp(e):
    return error('Runtime Exception: {}'.format(str(e)), 500)

def name_format_resp(entity, name):
    return error(message="The {} name [{}] provided is invalid/wrong format".format(entity, name), code=status_400)

def name_length_resp(entity, name):
    return error(message="The {} name [{}] provided is too short".format(entity, name), code=status_400)

def exists_resp(entity, value, field):
    return error('Conflict: {} with {} as {} already exists'.format(entity, value, field), 409)