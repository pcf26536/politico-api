from flask import request, Blueprint
from api.ver2.utils.strings import user_id_key, vote_key
from api.strings import post_method, status_201
from api.ver1.ballot.strings import candidate_key, createdOn_key, createdBy_key
from api.ver1.utils import check_form_data, no_entry_resp, field_missing_resp, error, success
from api.ver2.models.votes import Vote
from api.ver1.offices.strings import office_key
import traceback

vote_bp = Blueprint('vote', __name__)


@vote_bp.route('/votes/', methods=[post_method])
def votes():
    fields = [user_id_key, createdBy_key, createdOn_key, candidate_key, office_key]
    data = check_form_data(vote_key, request, fields)
    if data:
        try:
            vote = Vote(
                created_by=data[createdBy_key],
                created_on=data[createdOn_key],
                office_id=data[office_key],
                candidate_id=data[candidate_key]
            )
            print(type(int(data[createdBy_key])))
        except Exception as e:
            return field_missing_resp(vote_key, fields, e.args[0])
        try:
            if vote.validate_vote():
                vote.create()
                return success(status_201, [vote.to_json()])
            else:
                return error(vote.message, vote.code)
        except Exception as e:
            return error('runtime exception: {}, {}'.format(e.args[0], traceback.print_exc()), 500)
    else:
        return no_entry_resp(vote_key, fields)
