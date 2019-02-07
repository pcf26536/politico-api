from flask import Blueprint, request
from api.ver1.utils import error, no_entry_resp, field_missing_resp, method_not_allowed, runtime_error_resp, not_found_resp
from api.ver1.validators import validate_dict, validate_id
from api.strings import name_key, post_method, get_method, patch_method, delete_method, ok_str
from .strings import hqAddKey, logoUrlKey, party_key
from api.ver1.parties.controllers import PartyCont

party_bp = Blueprint('parties', __name__) # init the blueprint for parties module

@party_bp.route('/parties', methods=[post_method, get_method])
def add_or_get_all_ep():
    if request.method == post_method:
        """ create party endpoint """
        
        data = request.get_json()
        form_data = request.form
        fields = [name_key, hqAddKey, logoUrlKey]
        if not data or not len(data):
            if form_data:
                data = form_data
            else:
                return no_entry_resp(party_key, fields)
        try:
            validate_dict(data, party_key)
            name = data[name_key]
            hq_address = data[hqAddKey]
            logo_url = data[logoUrlKey]
        except KeyError as e:
            return field_missing_resp(party_key, fields, e.args[0])

        party = PartyCont(name=name, hqAddress=hq_address, logoUrl=logo_url)
        return party.add_party()

    elif request.method == get_method:
        return PartyCont().get_parties()
    else:
        return method_not_allowed(request.method)


@party_bp.route('/parties/<int:id>', methods=[delete_method, get_method])
def get_or_delete_ep(id):
    try:
        party = PartyCont(Id=id)
        if validate_id(party_key, id) == ok_str:
            if request.method == get_method:
                return party.get_party()
            elif request.method == delete_method:
                return party.delete_party()
            else:
                return method_not_allowed(request.method)
        return not_found_resp(party_key)  
    except Exception as e:
        return runtime_error_resp(e)


@party_bp.route('/parties/<int:id>/name', methods=[patch_method])
def edit_ep(id):
    try:
        if request.method == patch_method:
            if validate_id(party_key,id) == ok_str:
                data = request.get_json()
                if not data:
                    data = request.form
                new_name = data[name_key]
                party = PartyCont(Id=id, name=new_name)
                return party.edit_party()
        else:
            return method_not_allowed(request.method)
    except Exception as e:
        return runtime_error_resp(e)
