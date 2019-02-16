from flask import request, Blueprint
from api.ver2.utils.strings import evidence_key, petition_key
from api.strings import post_method, status_201
from api.ver1.ballot.strings import createdOn_key, createdBy_key, body_key
from api.ver1.utils import check_form_data, no_entry_resp, field_missing_resp, error, success
from api.ver1.offices.strings import office_key
from api.ver2.models.petitions import Petition


petitions_bp = Blueprint('petitions_bp', __name__)


@petitions_bp.route('/petitions/', methods=[post_method])
def petitions():
    fields = [createdBy_key, createdOn_key, office_key, body_key, evidence_key]
    data = check_form_data(petition_key, request, fields)
    if data:
        try:
            petition = Petition(
                created_by=data[createdBy_key],
                created_on=data[createdOn_key],
                office_id=data[office_key],
                body=data[body_key],
                evidence=data[evidence_key]
            )
            if petition.validate_petition():
                petition.create()
                return success(status_201, [petition.to_json()])
            else:
                return error(petition.message, petition.code)
        except Exception as e:
            return field_missing_resp(petition_key, fields, e.args[0])
    else:
        return no_entry_resp(petition_key, fields)
