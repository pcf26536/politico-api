from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.ver2.utils.strings import vote_key
from api.strings import post_method, status_201, get_method
from api.ver1.ballot.strings import candidate_key
from api.ver1.utils import check_form_data, no_entry_resp, \
    field_missing_resp, success, error
from api.ver2.models.votes import Vote
from api.ver2.utils.utilities import system_unavailable


vote_bp = Blueprint('vote', __name__)


@vote_bp.route('/votes/', methods=[post_method, get_method])
@jwt_required
def votes():
    try:
        if request.method == post_method:
            fields = [candidate_key]
            data = check_form_data(vote_key, request, fields)
            if data:
                try:
                    user = get_jwt_identity()
                    vote = Vote(
                        created_by=user,
                        candidate_id=data[candidate_key]
                    )
                except IndexError as e:
                    return field_missing_resp(vote_key, fields, e.args[0])

                if vote.validate_vote():
                    data = vote.create()
                    return success(status_201, [data])
                else:
                    return error(vote.message, vote.code)
            else:
                return no_entry_resp(vote_key, fields)
        elif request.method == get_method:
            return success(200, [Vote().get_all_results()])
    except Exception as e:
        return system_unavailable(e)


@vote_bp.route('/votes/<int:id>', methods=[get_method])
@jwt_required
def user_votes(id):
    try:
        return success(200, [Vote().get_by('createdby', id)])
    except Exception as e:
        return system_unavailable(e)
