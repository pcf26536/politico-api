from flask import request, Blueprint
from api.ver2.utils.strings import user_id_key, vote_key
from api.strings import post_method, status_201
from api.ver1.ballot.strings import candidate_key, createdOn_key, createdBy_key
from api.ver1.utils import check_form_data, no_entry_resp, field_missing_resp, error, success
from api.ver1.offices.strings import office_id_str
from api.ver2.models.votes import Vote


vote = Blueprint('vote', __name__)


@vote.route('/votes/', methods=[post_method])
def vote():
    fields = [user_id_key, createdBy_key, createdOn_key, candidate_key, office_id_str]
    data = check_form_data(vote_key, request, fields)
    if data:
        try:
            pass
        except Exception as e:
            return field_missing_resp(vote_key, fields, e.args[0])
    else:
        return no_entry_resp(vote_key, fields)
