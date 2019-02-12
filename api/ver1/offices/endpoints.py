from flask import Blueprint, request
from api.ver1.utils import field_missing_resp, runtime_error_resp, not_found_resp, check_form_data, no_entry_resp
from api.ver1.offices.controllers import OfficeCont
from api.strings import name_key, post_method, get_method, type_key, ok_str
from api.ver1.offices.strings import office_key
from api.ver1.validators import validate_dict, validate_id


office_bp = Blueprint('offices', __name__) # init the blueprint for offices module


@office_bp.route('/offices', methods=[post_method, get_method])
def add_or_get_all_ep():
    if request.method == post_method:
        fields = [name_key, type_key]
        data = check_form_data(office_key, request, fields)
        if not data:
            return no_entry_resp(office_key, fields)
        try:
            status = validate_dict(data, office_key)
            if not status == ok_str:
                return status
            name = data[name_key]
            office_type = data[type_key]
            office = OfficeCont(name=name, office_type=office_type)
            return office.add_office()
        except KeyError as e:
            return field_missing_resp(office_key, fields, e.args[0])

    elif request.method == get_method:
        return OfficeCont().get_offices()


@office_bp.route('/offices/<int:id>', methods=[get_method])
def get_office_ep(id):
    """" get specific offce by id """
    try:
        if validate_id(office_key, id) == ok_str:
            office = OfficeCont(Id=id)
            if request.method == get_method:
                return office.get_office()
        return not_found_resp(office_key)
    except Exception as e:
        return runtime_error_resp(e)
