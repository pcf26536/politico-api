from flask import request, Blueprint
from api.ver1.utils import field_missing_resp, runtime_error_resp, not_found_resp, check_form_data, no_entry_resp
from api.ver1.validators import validate_dict, validate_id
from api.strings import name_key, post_method, get_method, delete_method, ok_str
from .strings import hqAddKey, logoUrlKey, party_key
from api.ver1.parties.controllers import PartyCont

party_v1 = Blueprint('parties_v1', __name__)


@party_v1.route('/parties', methods=[post_method, get_method])
def add_or_get_all_ep():
    if request.method == post_method:
        """ create party endpoint """
        fields = [name_key, hqAddKey, logoUrlKey]
        data = check_form_data(party_key, request, fields)
        if not data:
            return no_entry_resp(party_key, fields)
        try:
            status = validate_dict(data, party_key)
            if not status == ok_str:
                return status
            name = data[name_key]
            hq_address = data[hqAddKey]
            logo_url = data[logoUrlKey]
            party = PartyCont(name=name, hqAddress=hq_address, logoUrl=logo_url)
            return party.add_party()
        except KeyError as e:
            return field_missing_resp(party_key, fields, e.args[0])

    elif request.method == get_method:
        return PartyCont().get_parties()


@party_v1.route('/parties/<int:id>', methods=[delete_method, get_method])
def get_or_delete_ep(id):
    try:
        party = PartyCont(Id=id)
        if validate_id(party_key, id) == ok_str:
            if request.method == get_method:
                return party.get_party()
            elif request.method == delete_method:
                return party.delete_party()
        not_found_resp(party_key)
    except Exception as e:
        return runtime_error_resp(e)


@party_v1.route('/parties/<int:id>/name', methods=['PATCH'])
def edit_ep(id):
    if request.method == 'PATCH':
        if validate_id(party_key,id) == ok_str:
            data = request.get_json()
            if not data:
                data = request.form
            new_name = data[name_key]
            party = PartyCont(Id=id, name=new_name)
            return party.edit_party()
