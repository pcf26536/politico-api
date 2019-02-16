from flask import request, Blueprint
from api.ver1.utils import field_missing_resp, runtime_error_resp, \
    not_found_resp, check_form_data, no_entry_resp, success, error
from api.ver2.models.offices import Office
from api.strings import name_key, post_method, get_method, type_key, ok_str
from api.ver1.offices.strings import office_key

office_v2 = Blueprint('offices_v2', __name__)


@office_v2.route('/offices', methods=[post_method, get_method])
def add_or_get_all_ep():
    if request.method == post_method:
        fields = [name_key, type_key]
        data = check_form_data(office_key, request, fields)
        if not data:
            return no_entry_resp(office_key, fields)
        try:
            name = data[name_key]
            office_type = data[type_key]
            office = Office(name=name, office_type=office_type)
            if office.validate_office():
                return success(201, [office.to_json()])
            else:
                return error(office.message, office.code)
        except KeyError as e:
            return field_missing_resp(office_key, fields, e.args[0])

    elif request.method == get_method:
        data = []
        offices = Office().get_all()
        for office in offices:
            data.append(office.to_json())
        return success(200, data)


@office_v2.route('/offices/<int:id>', methods=[get_method])
def get_office_ep(id):
    """" get specific office by id """
    try:
        office = Office(Id=id)
        if office.get_by('id', id):
            o = office.get_by('id', id)
            return success(200, [o.to_json()])
        else:
            return not_found_resp(office_key)
    except Exception as e:
        return runtime_error_resp(e)
