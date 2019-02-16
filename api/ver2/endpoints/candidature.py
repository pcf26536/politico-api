from flask import request, Blueprint
from flask_jwt_extended import (jwt_required)
from api.strings import post_method, status_201, get_method
from api.ver1.utils import check_form_data, no_entry_resp, \
    field_missing_resp, error, success, runtime_error_resp, not_found_resp
from api.ver2.utils.strings import user_id_key
from api.ver1.parties.strings import party_id_key, party_key
from api.ver1.offices.strings import office_key
from api.ver1.ballot.strings import candidate_key
from api.ver2.utils import is_not_admin
from api.ver2.models.candidates import Candidate
from api.ver2.models.votes import Vote
import traceback

candids = Blueprint('candidates', __name__)


@candids.route('/office/<int:id>/register', methods=[post_method])
@jwt_required
def register(id):
    if is_not_admin():
        return is_not_admin()
    fields = [party_key, candidate_key]
    data = check_form_data(candidate_key, request, fields)
    if data:
        try:
            candidate = Candidate(
                party_id=data[party_key],
                office_id=id,
                candid_id=data[candidate_key]
            )
        except Exception as e:
            return field_missing_resp(candidate_key, fields, e.args[0])
        try:
            if candidate.validate_candidate():
                candidate.create()
                return success(status_201, [candidate.to_json()])
            else:
                return error(candidate.message, candidate.code)
        except Exception as e:
            return error('runtime exception: {}, {}'.format(e.args[0], traceback.print_exc()), 500)
    else:
        return no_entry_resp(candidate_key, fields)


@candids.route('/office/<int:id>/results', methods=[get_method])
def results(id):
    try:
        votes = Vote(office_id=id).get_by(office_key, id)
        if not votes:
            return error('The specified office has no results yet!', 404)
        data = []
        for vote in votes:
            data.append(vote.to_json())
        return success(200, data)
    except Exception as e:
        return runtime_error_resp(e)
