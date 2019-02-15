from flask import request, Blueprint
from api.ver1.utils import field_missing_resp, runtime_error_resp, \
    not_found_resp, check_form_data, no_entry_resp, error, success
from api.strings import name_key, post_method, get_method, delete_method
from api.ver1.parties.strings import hqAddKey, logoUrlKey, party_key
from api.ver2.models.parties import Party

party_v2 = Blueprint('parties_v2', __name__)


@party_v2.route('/parties', methods=[post_method, get_method])
def add_or_get_all_ep():
    if request.method == post_method:
        """ create party endpoint """
        fields = [name_key, hqAddKey, logoUrlKey]
        data = check_form_data(party_key, request, fields)
        if not data:
            return no_entry_resp(party_key, fields)
        try:
            name = data[name_key]
            hq_address = data[hqAddKey]
            logo_url = data[logoUrlKey]
            party = Party(name=name, hqAddress=hq_address, logoUrl=logo_url)
            if party.validate_party():
                return success(201, [party.to_json()])
            else:
                return error(party.message, party.code)
        except KeyError as e:
            return field_missing_resp(party_key, fields, e.args[0])

    elif request.method == get_method:
        data = []
        parties = Party().get_all()
        for party in parties:
            data.append(party.to_json())
        return success(200, data)


@party_v2.route('/parties/<int:id>', methods=[delete_method, get_method])
def get_or_delete_ep(id):
    try:
        party = Party(Id=id)
        if party.get_by('id', id):
            if request.method == get_method:
                p = party.get_by('id', id)
                return success(200, [party])
            elif request.method == delete_method:
                party.delete(id)
        else:
            not_found_resp(party_key)
    except Exception as e:
        return runtime_error_resp(e)


@party_v2.route('/parties/<int:id>/name', methods=['PATCH'])
def edit_ep(id):
    if request.method == 'PATCH':
        party = Party().get_by('id', id)
        if party:
            party.to_json()
            data = request.get_json()
            if not data:
                data = request.form
            new_name = data[name_key]
            party.patch('name', new_name, id)
            return success(200, [party.to_json()])
        return not_found_resp(party_key)
