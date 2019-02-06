from flask import Blueprint, jsonify, request
from api.ver1.utils import error, success
from api.ver1.offices.controllers import Office
from api.strings import *
from .strings import *
from api.tests.strings import *

office_bp = Blueprint('offices', __name__) # init the blueprint for offices module

@office_bp.route('/offices', methods=[post_method, get_method])
def add_or_get_all_ep():
    if request.method == post_method:
        """ create office endpoint """
        data = request.get_json()
        form_data = request.form
        #return error(str(len(data)), 201)
        if not data or not len(data):
            if form_data:
                data = form_data
            else:
                return error(no_data, status_400)
        try:
            name = data[name_key]
            office_type = data[type_key]
        except KeyError as e:
            return error("{} field is required".format(e.args[0]), status_400)

        office = Office(name=name, type=office_type)
        return office.add_office()

    elif request.method == get_method:
        """ get all offices endpoint"""
        return Office().get_offices()


@office_bp.route('/offices/<int:id>', methods=[get_method])
def get_office_ep(id):
    try:
        office = Office(id=id)
        if request.method == get_method:
            return office.get_office()
    except Exception as e:
        return error(str(e), 500)
