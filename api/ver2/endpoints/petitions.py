from flask import request, Blueprint
from api.ver2.utils.strings import user_id_key, vote_key
from api.strings import post_method, status_201
from api.ver1.ballot.strings import candidate_key, createdOn_key, createdBy_key, body_key
from api.ver1.utils import check_form_data, no_entry_resp, field_missing_resp, error, success
from api.ver1.offices.strings import office_id_str
from api.ver2.models.petitions import Petition
from api.ver2.utils.strings import evidence_key


petitions = Blueprint('petitions', __name__)


@petitions.route('/petitions/', methods=[post_method])
def votes():
    fields = [createdBy_key, createdOn_key, office_id_str, body_key, evidence_key]
    data = check_form_data(vote_key, request, fields)
    if data:
        try:
            petition = Petition(
                created_by=data[createdBy_key],
                created_on=data[createdOn_key],
                office_id=data[office_id_str],
                candidate_id=data[candidate_key]
            )
            if vote.validate_vote():
                vote.create()
                return success(status_201, [vote.to_json()])
            else:
                return error(vote.message, vote.code)
        except Exception as e:
            return field_missing_resp(vote_key, fields, e.args[0])
    else:
        return no_entry_resp(vote_key, fields)
