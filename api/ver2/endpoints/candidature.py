from flask import request, Blueprint
from flask_jwt_extended import (jwt_required)
from api.strings import post_method, status_201
from api.ver1.utils import check_form_data, no_entry_resp, field_missing_resp, error, success
from api.ver2.utils.strings import user_id_key
from api.ver1.parties.strings import party_id_key
from api.ver1.ballot.strings import candidate_key
from api.ver2.utils import is_not_admin
from api.ver2.models.candidates import Candidate

register = Blueprint('api_ver2', __name__)


@register.route('/office/<int:id>/register', methods=[post_method])
@jwt_required
def register(id):
    if is_not_admin():
        return is_not_admin()
    fields = [party_id_key, user_id_key]
    data = check_form_data(candidate_key, request, fields)
    if data:
        try:
            candidate = Candidate(
                party_id=data[party_id_key],
                office_id=id,
                candid_id=data[user_id_key]
            )
            if candidate.validate_candidate():
                candidate.create()
                return success(status_201, [candidate.to_json()])
            else:
                return error(candidate.message, candidate.code)
        except Exception as e:
            return field_missing_resp(candidate_key, fields, e.args[0])
    else:
        return no_entry_resp(candidate_key, fields)
