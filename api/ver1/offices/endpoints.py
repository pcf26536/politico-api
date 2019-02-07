from flask import Blueprint, jsonify, request
from api.ver1.utils import error, success, no_entry_resp, field_missing_resp, method_not_allowed
from api.ver1.offices.controllers import cOffice
from api.strings import name_key, post_method, get_method, status_400, type_key, ok_str
from api.tests.strings import no_data
from api.ver1.offices.strings import office_key
from api.ver1.validators import validate_dict, validate_id

office_bp = Blueprint('offices', __name__) # init the blueprint for offices module

@office_bp.route('/offices', methods=[post_method, get_method])
def add_or_get_all_ep():
    if request.method == post_method:
        """ create office endpoint """
        data = request.get_json()
        form_data = request.form # check for any form data
        fields = [name_key, type_key]
        if not data or not len(data):
            if form_data:
                data = form_data
            else:
                return no_entry_resp(office_key, fields)
        try:
            validate_dict(data, office_key)
            name = data[name_key]
            office_type = data[type_key]
        except KeyError as e:
            return field_missing_resp(office_key, fields, e.args[0])

        office = cOffice(name=name, type=office_type)
        return office.add_office()

    elif request.method == get_method:
        """ get all offices endpoint"""
        return cOffice().get_offices()
    
    else:
        return method_not_allowed(request.method)
        

@office_bp.route('/offices/<int:id>', methods=[get_method])
def get_office_ep(office_id):
    """" get specific offce by id """
    try:
        if validate_id(office_key, office_id) == ok_str:
            office = cOffice(id=office_id)
            if request.method == get_method:
                return office.get_office()
            else:
                return method_not_allowed(request.method)
    except Exception as e:
        return error(str(e), 500)
