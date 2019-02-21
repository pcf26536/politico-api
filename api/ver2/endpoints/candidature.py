from flask import request, Blueprint
from flask_jwt_extended import (jwt_required)
from api.strings import post_method, status_201, get_method
from api.ver1.utils import check_form_data, no_entry_resp, \
    field_missing_resp, error, success
from api.ver1.parties.strings import party_key
from api.ver1.offices.strings import office_key
from api.ver1.ballot.strings import candidate_key
from api.ver2.utils import is_not_admin
from api.ver2.models.candidates import Candidate
from api.ver2.models.votes import Vote
from api.ver2.utils.utilities import system_unavailable

candids = Blueprint('candidates', __name__)


@candids.route('/office/<int:id>/register', methods=[post_method, get_method])
@jwt_required
def register(id):
    try:
        if request.method == post_method:
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
                if candidate.validate_candidate():
                    candidate.create()
                    return success(status_201, [candidate.to_json()])
                else:
                    return error(candidate.message, candidate.code)
            else:
                return no_entry_resp(candidate_key, fields)
        elif request.method == get_method:
            return success(200, Candidate().get_by_param('office', id))
    except Exception as e:
        return system_unavailable(e)


@candids.route('/candidates', methods=[get_method])
@jwt_required
def candidates():
    try:
        return success(200, Candidate().get_all())
    except Exception as e:
        return system_unavailable(e)


@candids.route('/office/<int:id>/result', methods=[get_method])
def results(id):
    try:
        print(Vote().get_by(office_key, id))
        if Vote().get_by(office_key, id):
            votes = Vote(
                office_id=id
            ).get_office_result()
            if not votes:
                return error('The specified office has no results yet!', 404)
            data = []
            for vote in votes:
                data.append(vote)
            return success(200, data)
        else:
            return error('Voting for the specified '
                         'office has not commenced yet!', 404)
    except Exception as e:
            return system_unavailable(e)
