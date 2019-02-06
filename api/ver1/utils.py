from flask import make_response, jsonify
from api.strings import *

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
