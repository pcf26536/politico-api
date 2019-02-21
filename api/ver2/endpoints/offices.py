from flask import request, Blueprint
from flask_jwt_extended import (jwt_required)
from api.ver1.utils import field_missing_resp, \
    not_found_resp, check_form_data, no_entry_resp, success, error
from api.ver2.models.offices import Office
from api.strings import name_key, post_method, get_method, type_key, delete_method
from api.ver1.offices.strings import office_key
from api.ver2.utils import is_not_admin
from api.ver2.utils.utilities import system_unavailable
from api.ver2.utils.validators import invalid_name

office_v2 = Blueprint('offices_v2', __name__)


@office_v2.route('/offices', methods=[post_method, get_method])
@jwt_required
def add_or_get_all_ep():
    try:
        if is_not_admin():
            return is_not_admin()
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
                    office.create()
                    return success(201, [office.to_json()])
                else:
                    return error(office.message, office.code)
            except KeyError as e:
                return field_missing_resp(office_key, fields, e.args[0])

        elif request.method == get_method:
            data = []
            offices = Office().get_all()
            for office in offices:
                data.append(office)
            return success(200, data)
    except Exception as e:
            return system_unavailable(e)


@office_v2.route('/offices/<int:id>', methods=[get_method, delete_method])
@jwt_required
def get_office_delete_ep(id):
    """" get specific office by id """
    try:
        if request.method == get_method:
            office = Office(Id=id)
            if office.get_by('id', id):
                o = office.get_by('id', id)
                return success(200, [o])
            else:
                return not_found_resp(office_key)
        elif request.method == delete_method:
            office = Office(Id=id)
            if office.get_by('id', id):
                p = office.get_by('id', id)
                if request.method == get_method:
                    return success(200, [p])
                elif request.method == delete_method:
                    if is_not_admin():
                        return is_not_admin()
                    office.delete(id)
                    return success(
                        200, [
                            {'message': p['name'] + ' deleted successfully'}])
            else:
                return not_found_resp(office_key)
    except Exception as e:
        return system_unavailable(e)


@office_v2.route('/offices/<int:id>/name', methods=['PATCH'])
@jwt_required
def edit_ep(id):
    try:
        if is_not_admin():
            return is_not_admin()
        if request.method == 'PATCH':
            office = Office().get_by('id', id)
            if office:
                fields = [name_key]
                data = check_form_data(office_key, request, fields)
                if not data:
                    return error(
                        "No data was provided,"
                        " fields [name] required to edit office", 400)
                new_name = data[name_key]
                if Office().get_by('name', new_name):
                    return error('Name already exists', 409)
                invalid = invalid_name(new_name, office_key)
                if invalid:
                    return error(invalid['message'], invalid['code'])
                new = Office(Id=id).patch('name', new_name, id)
                return success(200, [new])
            return not_found_resp(office_key)
    except Exception as e:
        return system_unavailable(e)
