from flask import Blueprint, request
from api.ver1.utils import error
from api.strings import name_key, post_method, get_method, status_400, patch_method, delete_method
from .strings import hqAddKey, logoUrlKey
from api.ver1.parties.controllers import cParty

party_bp = Blueprint('parties', __name__) # init the blueprint for parties module

@party_bp.route('/parties', methods=[post_method, get_method])
def add_or_get_all_ep():
    if request.method == post_method:
        """ create party endpoint """
        data = request.get_json()
        form_data = request.form
        #return error(str(len(data)), 201)
        if not data or not len(data):
            if form_data:
                data = form_data
            else:
                return error("No data was provided", status_400)
        try:
            name = data[name_key]
            hq_address = data[hqAddKey]
            logo_url = data[logoUrlKey]
        except KeyError as e:
            return error("{} field is required".format(e.args[0]), status_400)

        party = cParty(name=name, hqAddress=hq_address, logoUrl=logo_url)
        return party.add_party()

    elif request.method == get_method:
        return cParty().get_parties()

@party_bp.route('/parties/<int:id>', methods=[delete_method, get_method])
def get_or_delete_ep(id):
    try:
        party = cParty(id=id)
        if request.method == get_method:
            return party.get_party()
        elif request.method == delete_method:
            return party.delete_party()
    except Exception as e:
        return error(str(e), 500)


@party_bp.route('/parties/<int:id>', methods=[patch_method])
def edit_ep(id):
    try:
        data = request.get_json()
        data = request.form
        new_name = data[name_key]
        party = cParty(id=id, name=new_name)
        return party.edit_party()
    except Exception as e:
        return error(str(e), 500)
