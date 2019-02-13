from api.ver1.ballot.models import petitions
from api.ver1.ballot.strings import createdOn_key, createdBy_key, body_key
from api.ver2.utils.strings import evidence_key, evidence_value
from api.ver1.offices.strings import office_key
from api.strings import id_key

correct_petition = petitions[0]
del correct_petition[id_key]
correct_petition[evidence_key] = evidence_value

petition_with_missing_key = correct_petition
del petition_with_missing_key[createdOn_key]

petition_with_wrong_user_id = correct_petition
petition_with_wrong_user_id[createdBy_key] = 55

petition_with_wrong_date_format = correct_petition
petition_with_wrong_date_format[createdOn_key] = '12th March 18'

petition_with_wrong_office_id = correct_petition
petition_with_wrong_office_id[office_key] = 55

petition_with_wrong_body_format = correct_petition
petition_with_wrong_body_format[body_key] = '!!@#$%%^^&&*(()'

petition_with_no_evidence = correct_petition
del petition_with_no_evidence[evidence_key]

petition_with_wrong_evidence_format = correct_petition
petition_with_wrong_evidence_format[evidence_key] = ['fdffdfd.asd', 'image.wemmm']
