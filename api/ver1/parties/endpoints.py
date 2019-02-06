from flask import Blueprint, jsonify, request
from api.ver1.utils import error, success
from api.ver1.parties.controllers import Party
from api.strings import *
from .strings import *

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

        party = Party(name=name, hqAddress=hq_address, logoUrl=logo_url)
        return party.add_party()

    elif request.method == get_method:
        return Party().get_parties()
        